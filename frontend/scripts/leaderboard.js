const API = "http://localhost:5001/leaderboard";

document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => switchTab(tab));
});

function switchTab(tab) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");

    const target = tab.dataset.tab;

    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    document.getElementById(target).classList.add("active");

    loadLeaderboard(target);
}

// -------- LOAD LEADERBOARD DATA --------

async function loadLeaderboard(type) {
    const res = await fetch(`${API}/${type}`);
    const json = await res.json();

    console.log(type, json);

    if (!json.data || !json.data.leaderboard) return;

    const rows = json.data.leaderboard;

    if (type === "authors") {
        renderAuthors(rows);
    } else {
        renderRecipes(type, rows);
    }
}

// -------- RENDER RECIPE LEADERBOARDS --------

function renderRecipes(type, rows) {
    const list = document.getElementById(`${type}-list`);
    list.innerHTML = "";

    rows.forEach((r, i) => {
        list.innerHTML += `
            <li>
                ${i + 1}. 
                <span class="inline-block-item">${r.title}</span>
                <span class="inline-block-item">${r.author}</span>
                <span class="inline-block-item likes">${r.likes}</span>
            </li>
        `;
    });
}

// -------- RENDER AUTHOR LEADERBOARD --------

function renderAuthors(rows) {
    const list = document.getElementById("authors-list");
    list.innerHTML = "";

    rows.forEach((r, i) => {
        list.innerHTML += `
            <li>
                ${i + 1}. 
                <span class="inline-block-item">${r.author}</span>
                <span class="inline-block-item likes">${r.total_likes}</span>
            </li>
        `;
    });
}


loadLeaderboard("weekly");
