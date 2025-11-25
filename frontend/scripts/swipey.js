const API_BASE = "http://localhost:5001";
const userID = localStorage.getItem("tastebuddin_user_id");

if (!userID) {
    window.location.href = "sign-in.html"; // changed
}

// new fetch functionality
fetch(`${API_BASE}/feed/${userID}`)
    .then(res => res.json())
    .then(data => {
        console.log("User feed: ", data);
        renderFeed(data.data);
    })


// variables for the animation
let recipes = [];
let idx = 0;
let startX, currX;
let dragging = false;

// references to doc elements
let titleRef = document.querySelector("#recipe-title");
let imgEl = document.querySelector("#recipe-image");
let descEl = document.querySelector("#recipe-overview");
let ingEl = document.querySelector("#recipe-ingredient-list");
let dirEl = document.querySelector("#recipe-steps-list");
let timeEl = document.querySelector("#recipe-est-time");


// render the feed
function renderFeed(feedData) {
    console.log("Rendering feed:", feedData);

    if (!feedData || feedData.length === 0) {
        showDefault();
        return;
    }

    // Save backend feed into global recipes list
    recipes = feedData;

    // reset index
    idx = 0;

    // show first recipe
    showRecipe();
}

function showDefault() {
    // TODO: write something to show default and be like
    // no recipes :(
    return;
}

function showRecipe() {
    if (recipes.length === 0) return showDefault();

    const r = recipes[idx];

    titleRef.innerHTML = r.title || "Untitled Recipe";

    // photo
    if (r.photopath) {
        imgEl.src = r.photopath;
        imgEl.style.display = "block";
    } else {
        imgEl.src = "default-resources/empty-dish.jpg";
    }

    // description
    descEl.innerHTML = r.description || "(No description)";

    // ingredients: array → HTML list
    ingEl.innerHTML = (r.ingredients || [])
        .map(i => `<p>${i}</p>`)
        .join("");

    // directions: array → HTML list
    dirEl.innerHTML = (r.directions || [])
        .map(step => `<p>${step}</p>`)
        .join("");

    // estimated time
    timeEl.innerHTML = r.minutestocomplete
        ? `${r.minutestocomplete} Minutes`
        : "N/A";
}



// TODO: make a copy, change this to "likeAnim"
function nextRecipe() {
    // whole bunch of animation stuff

    setTimeout(() => {
        idx = (idx + 1) % recipes.length;
        // more animation stuff
        showRecipe();
    }, 300);
}

async function like() {
    // current recipe
    const curr_idx = idx;
    const r = recipes[curr_idx];
    const route = `${API_BASE}/user/like`;

    // connect to backend, deliver recipe to be liked
    fetch(route, {
        method: "POST",
        headers: { "Content-Type": "recipe/json" },
        body: JSON.stringify({
            user_id: userID,
            recipe_id: r.recipe_id,
            author_id: r.author_id
        })
    });

    // move on to next recipe in the frontend
    nextRecipe();
}

function dislike() {

    // current recipe
    const curr_idx = idx;
    const r = recipes[curr_idx];
    const route = `${API_BASE}/user/dislike`;

    // connect to backend, deliver recipe to be liked
    fetch(route, {
        method: "POST",
        headers: { "Content-Type": "recipe/json" },
        body: JSON.stringify({
            user_id: userID,
            recipe_id: r.recipe_id,
        })
    });

    // move on to next recipe in the frontend
    nextRecipe();
}


// set what functions run for each button
document.getElementById("like-button").onclick = like;
document.getElementById("reject-button").onclick = dislike;

