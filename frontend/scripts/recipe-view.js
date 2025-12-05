
/* 
File: recipe-view.js
Purpose: Handles loading, parsing, and rendering of an individual recipe displayed
  on the recipe viewer page.
System Role: Front-end controller for dynamic recipe viewing. Interacts with the backend
  API, sanitizes/normalizes inconsistent recipe formats, and updates the DOM.
  Also manages fallback behavior when recipes cannot be found or loaded.
Edited Last: 2025-12-04
Authors: Sarah Temple
Modifications:
  - Added URL parameter parsing to load recipe by recipeid.
  - Added renderRecipe() to validate incoming backend data.
  - Added showDefault() fallback UI for missing or invalid recipes.
  - Improved steps/directions parsing to handle stringified arrays, mixed types,
    and nested stringified JSON.
  - Added dynamic HTML rendering for ingredients, allergens, and directions.
  - Connected “no recipe found” UI with #no-recipes and #recipe-card containers.

Uses:
  - API_BASE — backend endpoint for retrieving recipes.
  - HTML elements:
      #recipe-title, #recipe-image, #recipe-allergen-tags, #recipe-author-name,
      #recipe-likes, #recipe-overview, #recipe-ingredient-list,
      #recipe-steps-list, #recipe-est-time, #recipe-card, #no-recipes
  - URLSearchParams — reads ?recipeid=<id> from the page URL.
*/

const API_BASE = "http://localhost:5001";


const params = new URLSearchParams(window.location.search);
const id = params.get("recipeid");

fetch(`${API_BASE}/recipes/${id}`)
    .then(res => res.json())
    .then(data => {
        console.log("User feed: ", data);

        // FIX HERE:
        const recipe = Array.isArray(data.data) ? data.data : [data.data];

        renderRecipe(recipe);
    });


let titleRef = document.querySelector("#recipe-title");
let imgEl = document.querySelector("#recipe-image");
let alrgEl = document.querySelector("#recipe-allergen-tags");
let authEl = document.querySelector("#recipe-author-name");
let likesEl = document.querySelector("#recipe-likes");
let descEl = document.querySelector("#recipe-overview");
let ingEl = document.querySelector("#recipe-ingredient-list");
let dirEl = document.querySelector("#recipe-steps-list");
let timeEl = document.querySelector("#recipe-est-time");
let idx = 0;

function renderRecipe(feedData) {
    console.log("Rendering recipe:", feedData);

    if (!feedData || !Array.isArray(feedData) || feedData.length === 0) 
        {
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

    //allergens
    alrgEl.innerHTML = (r.dietaryrestrictions || [])
        .map(i => `<p>${i}</p>`)
        .join("");

    //author
    authEl.innerHTML = r.authorname || "(No Author Name)";
    
    //likes

    likesEl.textContent = r.likes ?? 0;



    // ingredients: array → HTML list
    ingEl.innerHTML = (r.ingredients || [])
        .map(i => `<p>${i}</p>`)
        .join("");

        let steps = r.directions || [];

        // if it's a string, try to parse JSON or wrap as single step
        if (typeof steps === "string") {
            try {
                const parsed = JSON.parse(steps);
                steps = Array.isArray(parsed) ? parsed : [steps];
            } catch {
                steps = [steps];
            }
        }
    
        // handle the case ['["step1","step2"]']
        if (Array.isArray(steps) &&
            steps.length === 1 &&
            typeof steps[0] === "string" &&
            steps[0].trim().startsWith("[")) {
            try {
                const parsedInner = JSON.parse(steps[0]);
                if (Array.isArray(parsedInner)) {
                    steps = parsedInner;
                }
            } catch {
                // leave as-is if parsing fails
            }
        }
    
        // directions: array → HTML list
        dirEl.innerHTML = steps
            .map(step => `<p>${step}</p>`)
            .join("");
    
        // estimated time
        timeEl.innerHTML = r.minutestocomplete
            ? `${r.minutestocomplete} Minutes`
            : "N/A";
}
