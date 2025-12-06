/* 
  File: leaderboard.js
  Created by: Sarah and Kadee
  Purpose:
    Controls the interactive leaderboard page, including tab switching
    and dynamic loading of leaderboard data for weekly, monthly, yearly,
    and author-based rankings. Also handles rendering and navigation
    from leaderboard entries to individual recipe pages.

  Main Features:
    - Tab switching system:
        • Clicking a tab activates the corresponding leaderboard view.
        • Only one tab and one content section are active at a time.
    - Fetches leaderboard data from backend API for:
        • /leaderboard/weekly
        • /leaderboard/monthly
        • /leaderboard/yearly
        • /leaderboard/authors
    - Renders two primary leaderboard types:
        1. Recipe leaderboards (weekly/monthly/yearly)
        2. Author leaderboard (total likes per author)
    - Enables clicking recipe rows to navigate to recipe-view.html.

  Dependencies:
    DOM Requirements:
      - Elements with class ".tab" for selectable tabs
          • Must contain data-tab="<contentID>"
      - Elements with class ".tab-content" for content panels
      - UL containers:
          • #weekly-list
          • #monthly-list
          • #yearly-list
          • #authors-list

  Key Functions:
    switchTab(tab):
        - Activates clicked tab, deactivates others.
        - Shows associated content panel.
        - Triggers loadLeaderboard() based on the tab's data attribute.

    loadLeaderboard(type):
        - Fetches leaderboard data from API.
        - Determines whether to render authors or recipe rankings.
        - Logs results for debugging.
        - Calls renderRecipes() or renderAuthors().

    renderRecipes(type, rows):
        - Renders ranked list of recipes.
        - Displays rank number, recipe title, author name, and like count.
        - Adds click handlers to navigate to recipe-view.html?recipeid=<id>.

    renderAuthors(rows):
        - Renders ranked list of authors.
        - Displays author name and total lifetime likes.

  Behavior Summary:
    - On page load:
        • Default leaderboard type (`weekly`) is loaded immediately.
    - Switching tabs fetches and redraws the proper leaderboard.
    - Leaderboard entries are dynamically built using innerHTML.
    - Recipe rows support click navigation; author rows do not navigate.
*/




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
            <li class="recipe-row" data-id="${r.recipeid}">
                ${i + 1}. 
                <span class="inline-block-item">${r.title}</span>
                <span class="inline-block-item">${r.author}</span>
                <span class="inline-block-item likes">${r.likes}</span>
            </li>
        `;
    });

    //  Make each row clickable
    document.querySelectorAll(".recipe-row").forEach(row => {
        row.addEventListener("click", () => {
            const id = row.dataset.id;
            window.location.href = `recipe-view.html?recipeid=${id}`;
        });
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
