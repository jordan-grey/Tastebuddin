/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
} 

function logOut() {
    let supabaseClient = null;
    async function loadSupabase() {
        try {
            // Load /frontend/config/config.json relative to pages/
            const cfg = await fetch("../config/config.json").then(res => res.json());

            supabaseClient = window.supabase.createClient(
                cfg.SUPABASE_URL,
                cfg.SUPABASE_ANON_KEY
            );

            console.log("Supabase loaded:", cfg.SUPABASE_URL);
        }catch (err) {
            console.error(err);
            alert("Failed to load Supabase config: " + err);
        }
    }
    async function signOut() {
        const { error } = await supabase.auth.signOut()
        if (error) {
            console.error(err);
            alert("Login failed: " + error.message);
            return;
        }
    };
    loadSupabase();
    signOut();

}