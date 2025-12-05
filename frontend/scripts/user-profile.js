/* 
  File: user-profile.js
  Created by: Evan
  Purpose: Handles profile page functionality including user auth, Supabase initialization, 
         loading public profile data, and managing profile photo uploads (file or camera).
  System Role: Front-end logic for user identity, avatar handling, and session management.

  Behavior Summary:
    - Attempts to load Supabase; falls back gracefully if config missing.
    - Ensures user is authenticated.
    - Loads + displays profile info.
    - Provides smooth avatar update flow (upload or camera).
    - Supports long-press activation on mobile.
    - All features degrade gracefully when Supabase is absent.
*/


// =============================
// SAFELY LOAD CONFIG
// =============================
async function loadConfig() {
  try {
    const res = await fetch("/config/config.json");
    if (!res.ok) throw new Error("Config not found");
    return await res.json();
  } catch (err) {
    console.warn("⚠️ config.json missing or unreadable. Supabase will not load.");
    return null;
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const cfg = await loadConfig();

  // =============================
  // INITIALIZE SUPABASE
  // =============================
  let supabase = null;

  if (cfg && cfg.SUPABASE_URL && (cfg.SUPABASE_ANON_KEY || cfg.SUPABASE_KEY)) {
    // support both keys but prefer anonymous public key
    const anon = cfg.SUPABASE_ANON_KEY || cfg.SUPABASE_KEY;
    supabase = window.supabase.createClient(cfg.SUPABASE_URL, anon);
  } else {
    console.warn("⚠️ Supabase not initialized due to missing config.");
  }

  // email is intentionally not shown in the profile view
  const idEl = document.getElementById("user-id");
  const totalLikesEl = document.getElementById("total-likes");
  const signoutBtn = document.getElementById("signout-btn");

  // =============================
  // LOAD USER DATA
  // =============================
  async function loadUser() {
    if (!supabase) {
      // Supabase not available — show placeholders and bail
      if (idEl) idEl.textContent = "Unavailable";
      if (totalLikesEl) totalLikesEl.textContent = "Unavailable";
      return;
    }

    const { data, error } = await supabase.auth.getUser();

    if (error || !data.user) {
      // Not logged in — redirect to sign-in page inside pages/
      window.location.href = "sign-in.html";
      return;
    }

    // store current user for later actions
    const currentUser = data.user;

    // If users_public does not provide a username, fall back to the email prefix

    // load additional public profile if available
    try {
      const { data: row, error: rErr } = await supabase
        .from('users_public')
        .select('username, pfp_path, created_at, total_likes')
        .eq('id', data.user.id)
        .maybeSingle();

      if (rErr) {
        console.warn('users_public fetch error:', rErr);
        showStatus('Could not load public profile: ' + (rErr.message || JSON.stringify(rErr)));
      }

      if (!rErr && row) {
        const usernameEl = document.getElementById('username');
        if (usernameEl) usernameEl.innerText = row.username || (currentUser.email ? currentUser.email.split('@')[0] : '(no username)');
        if (row.pfp_path) {
          const img = document.getElementById('profileImage');
          if (img) img.src = row.pfp_path;
        }
        if (totalLikesEl) totalLikesEl.innerText = row.total_likes ?? 0;
      } else {
        if (totalLikesEl) totalLikesEl.innerText = 0;
      }
      } catch (e) {
      console.warn('Failed to load users_public row', e);
        // fallback: set username from session email if present
        try {
          const usernameEl = document.getElementById('username');
          if (usernameEl) usernameEl.innerText = currentUser.email ? currentUser.email.split('@')[0] : '(no username)';
          if (totalLikesEl) totalLikesEl.innerText = 0;
        } catch (err) {}
    }
  }

  await loadUser();

  // =============================
  // SIGN OUT
  // =============================
  signoutBtn.addEventListener("click", async () => {
    if (!supabase) {
      alert("Supabase not initialized.");
      return;
    }

    await supabase.auth.signOut();
    window.location.href = "sign-in.html";
  });

  // --------------------
  // Profile picture upload + camera
  // --------------------
  const profileFile = document.getElementById('profileFile');
  const profileImage = document.getElementById('profileImage');
  const changePhotoBtn = document.getElementById('changePhotoBtn');
  const cameraModal = document.getElementById('cameraModal');
  const cameraVideo = document.getElementById('cameraVideo');
  const snapBtn = document.getElementById('snapBtn');
  const closeCamera = document.getElementById('closeCamera');

  // derive localKey based on current session user id (if available)
  let localKey = 'tastebuddin_profile_anonymous';
  try { const s = supabase ? (await supabase.auth.getUser()).data.user : null; if (s && s.id) localKey = 'tastebuddin_profile_' + s.id; } catch (e) {}

  // load from local storage if present
  try {
    const saved = localStorage.getItem(localKey);
    if (saved && profileImage) profileImage.src = saved;
  } catch (e) {}

  // click handlers
  if (profileImage) profileImage.addEventListener('click', () => profileFile.click());

  // dropdown menu and actions
  const photoMenu = document.getElementById('photoMenu');
  const useCameraBtn = document.getElementById('useCameraBtn');
  const uploadFileBtn = document.getElementById('uploadFileBtn');

  let isLongPressTriggered = false; // prevents click handling after long-press camera

  // open / close the small dropdown attached to the avatar actions
  function openPhotoMenu() {
    if (!photoMenu || !changePhotoBtn) return;
    photoMenu.style.display = 'block';
    photoMenu.setAttribute('aria-hidden', 'false');
    changePhotoBtn.setAttribute('aria-expanded', 'true');
    // listen for outside clicks (one-time)
    setTimeout(() => {
      document.addEventListener('click', outsideClickHandler);
      document.addEventListener('keydown', escKeyHandler);
    }, 10);
  }

  function closePhotoMenu() {
    if (!photoMenu || !changePhotoBtn) return;
    photoMenu.style.display = 'none';
    photoMenu.setAttribute('aria-hidden', 'true');
    changePhotoBtn.setAttribute('aria-expanded', 'false');
    document.removeEventListener('click', outsideClickHandler);
    document.removeEventListener('keydown', escKeyHandler);
  }

  function outsideClickHandler(e) {
    if (!photoMenu) return;
    if (!photoMenu.contains(e.target) && !changePhotoBtn.contains(e.target)) closePhotoMenu();
  }

  function escKeyHandler(e) {
    if (e.key === 'Escape') closePhotoMenu();
  }

  if (changePhotoBtn) changePhotoBtn.addEventListener('click', (ev) => {
    // if long press already triggered camera, ignore the click to avoid race
    if (isLongPressTriggered) {
      // reset the flag shortly after, so normal clicks resume
      setTimeout(() => { isLongPressTriggered = false; }, 50);
      return;
    }

    // toggle the small menu
    if (!photoMenu || photoMenu.style.display === 'block') closePhotoMenu(); else openPhotoMenu();
  });

  // long press (mobile) to open camera
  let pressTimer = null;
  if (changePhotoBtn) {
    changePhotoBtn.addEventListener('pointerdown', () => { pressTimer = setTimeout(() => { openCamera(); isLongPressTriggered = true; }, 300); });
    changePhotoBtn.addEventListener('pointerup', () => { if (pressTimer) { clearTimeout(pressTimer); pressTimer = null; } });
  }

  // menu option actions
  if (useCameraBtn) useCameraBtn.addEventListener('click', () => { closePhotoMenu(); openCamera(); });
  if (uploadFileBtn) uploadFileBtn.addEventListener('click', () => { closePhotoMenu(); profileFile.click(); });

  profileFile.addEventListener('change', async (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    // preview
    const reader = new FileReader();
    reader.onload = () => {
      profileImage.src = reader.result;
      try { localStorage.setItem(localKey, reader.result); } catch (err) {}
    };
    reader.readAsDataURL(f);

    // try to upload to Supabase Storage and update users_public if we can
    if (supabase) {
      try {
        // use current user id when creating filename
        const sessionUser = (await supabase.auth.getUser()).data.user;
        const uid = sessionUser ? sessionUser.id : 'anon';
        const fileName = `avatars/${uid}_${Date.now()}`;
        const upload = await supabase.storage.from('profile_images').upload(fileName, f, { upsert: true });
        if (upload.error) throw upload.error;
        const { data: urlData } = supabase.storage.from('profile_images').getPublicUrl(fileName);
        const publicUrl = urlData.publicUrl || (urlData && urlData?.publicUrl);
        if (publicUrl && sessionUser && sessionUser.id) {
          await supabase.from('users_public').update({ pfp_path: publicUrl }).eq('id', sessionUser.id);
        }
      } catch (err) {
        console.warn('Upload to storage failed — saved locally only', err?.message || err);
        // help the developer: if bucket not found, tell them exactly how to fix it
        if ((err && err.message && err.message.toLowerCase().includes('bucket')) || (err && err.status === 400)) {
          const msg = 'Upload failed: bucket not found or bad request. Create a Storage bucket named "profile_images" in Supabase or change the bucket name in the client.';
          console.info(msg);
          showStatus(msg);
        } else {
          showStatus('Upload failed (saved locally only): ' + (err?.message || String(err)));
        }
      }
    }
  });

  // showStatus helper – small UI message under the card
  function showStatus(message, isError = true) {
    try {
      const el = document.getElementById('profile-status');
      if (!el) return;
      el.style.display = 'block';
      el.style.color = isError ? '#a33' : '#0a6';
      el.innerText = message;
    } catch (e) { console.log('status show failed', e); }
  }

  function openCamera() {
    if (!cameraModal || !cameraVideo) return;
    cameraModal.style.display = 'flex';
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      .then(stream => { cameraVideo.srcObject = stream; cameraVideo.play(); cameraVideo._stream = stream; })
      .catch(err => { alert('Camera not available: ' + err.message); });
  }

  snapBtn && snapBtn.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = cameraVideo.videoWidth || 640;
    canvas.height = cameraVideo.videoHeight || 480;
    canvas.getContext('2d').drawImage(cameraVideo, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    profileImage.src = dataUrl;
    try { localStorage.setItem(localKey, dataUrl); } catch (err) {}
    if (cameraVideo._stream) cameraVideo._stream.getTracks().forEach(t => t.stop());
    cameraModal.style.display = 'none';
  });

  closeCamera && closeCamera.addEventListener('click', () => {
    if (cameraVideo._stream) cameraVideo._stream.getTracks().forEach(t => t.stop());
    cameraModal.style.display = 'none';
  });
});