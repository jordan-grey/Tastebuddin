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
    });


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
    console.log("No recipes left!");

    // Hide recipe card
    document.getElementById("recipe-card").style.display = "none";

    // Show "no more recipes"
    document.getElementById("no-recipes").style.display = "block";

    document.getElementById("like-button").disabled = true;
    document.getElementById("reject-button").disabled = true;
    return;
}


document.body.innerHTML.includes("no-recipes")



function showRecipe() {
    if (recipes.length === 0 || idx >= recipes.length || !recipes[idx]) {
        return showDefault();
    }

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
        idx += 1;

        if (idx >= recipes.length) {
            recipes = [];
            return showDefault();
        }
    
        showRecipe();
    }, 300);
}

async function like() {
    // current recipe
    if (recipes.length === 0 || !recipes[idx]) {
        return showDefault();
    }
    const curr_idx = idx;
    const r = recipes[curr_idx];
    if (!r) return showDefault();
    const route = `${API_BASE}/user/like`;
    const delivery = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: userID,
            recipeid: r.recipeid,
            author_id: r.authorid
        }),
    };
    // console.log("Current recipe: ", r);
    // console.log("Attempting to POST: ", delivery);
    // console.log("Attempted POST body: ", delivery.body);

    // connect to backend, deliver recipe to be liked
    await fetch(route, delivery);

    // move on to next recipe in the frontend
    nextRecipe();
}

async function dislike() {
    if (recipes.length === 0 || !recipes[idx]) {
        return showDefault();
    }

    // current recipe
    const curr_idx = idx;
    const r = recipes[curr_idx];
    if (!r) return showDefault();
    const route = `${API_BASE}/user/dislike`;
    const delivery = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: userID,
            recipe_id: r.recipeid,
        })
    };

    // console.log("Current recipe: ", r);
    // console.log("Attempting to POST: ", delivery);
    // console.log("Attempted POST body: ", delivery.body);

    // connect to backend, deliver recipe to be liked
    await fetch(route, delivery);

    // move on to next recipe in the frontend
    nextRecipe();
}


// set what functions run for each button
document.getElementById("like-button").onclick = like;
document.getElementById("reject-button").onclick = dislike;

