const API_BASE = "http://localhost:5001";
// const FEED_ENDPOINT = "/feed/sarah_test";

const userID = localStorage.getItem("tastebuddin_user_id");

if (!userID) {
    window.location.href = "signin.html"; // changed
}

// new fetch functionality
fetch('http://localhost:5001/feed/${userID}')
    .then(res => res.json())
    .then(data => {
        console.log("User feed: ", data),
        renderFeed(data.data);
    })

let recipes = [];
let idx = 0;

// rewrite this to be different
let card = document.getElementById("recipe-info");
let startX, currX;
let dragging = false;

async function loadRecipes() {
    const res = await fetch(API_BASE + FEED_ENDPOINT);
    const json = await res.json();
    recipes = json.data || [];
    showRecipe();
}

function showDefault() {
    // TODO: write something to show default and be like
    // no recipes :(
    return;
}

function showRecipe() {
    if (recipes.length === 0) {
        card.querySelector("#recipe-title").innerHTML = "No Recipes Available!";
        return; // show error message and then exit
    }

    // populate the html with information
    let r = recipes[idx];
    

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

function like() {
    nextRecipe();
}

function dislike() {
    nextRecipe();
}

document.getElementById("like-button").onclick = like;
document.getElementById("reject-button").onclick = dislike;

loadRecipes();

