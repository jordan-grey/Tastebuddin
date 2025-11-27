const API_BASE = "http://localhost:5001";



const params = new URLSearchParams(window.location.search);
const id = params.get("recipeid");

fetch(`${API_BASE}/recipes/${id}`)
    .then(res => {res.json()
        console.log("User feed: ", res);
    })
/*.then(data => {
        console.log("User feed: ", data);
        renderFeed(data.data); 
    })   */

let titleRef = document.querySelector("#recipe-title");
let imgEl = document.querySelector("#recipe-image");
let descEl = document.querySelector("#recipe-overview");
let ingEl = document.querySelector("#recipe-ingredient-list");
let dirEl = document.querySelector("#recipe-steps-list");
let timeEl = document.querySelector("#recipe-est-time");

function renderRecipe(feedData) {
    console.log("Rendering recipe:", feedData);

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
    console.log("Recipe Not Found!");

    // Hide recipe card
    document.getElementById("recipe-card").style.display = "none";

    // Show "no more recipes"
    document.getElementById("no-recipes").style.display = "block";
    return;
}

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
