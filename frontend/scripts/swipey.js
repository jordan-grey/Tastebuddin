const API_BASE = "http://localhost:5001";
// const FEED_ENDPOINT = "/feed/sarah_test";

const userID = localStorage.getItem("tastebuddin_user_id");

if (!userID) {
    window.location.href = "sign-in.html"; // changed
}

// // new fetch functionality
// fetch(`http://localhost:5001/feed/${userID}`)
//     .then(res => res.json())
//     .then(data => {
//         console.log("User feed: ", data);
//         // renderFeed(data.data);
//     })

// let recipes = [
//         {
//             "title": "UnitTest Brownie",
//             "description": "A chocolate brownie created by tests.",
//             "ingredients": ["flour", "sugar", "cocoa"],
//             "directions": ["mix", "bake"],
//             "category": "dessert",
//             "dietaryrestrictions": ["vegetarian"],
//             "minutestocomplete": 30,
//             "authorid": "fce74316-e465-412b-8e57-8ff7cbd72d3d",
//             "authorname": "test_kadee",
//             "photopath": "https://upload.wikimedia.org/wikipedia/commons/6/68/Chocolatebrownie.JPG"

//         },
//         {
//         "title": "Fluffy Buttermilk Pancakes",
//             "description": "Classic fluffy pancakes perfect for a weekend breakfast.",
//             "ingredients": ["flour","buttermilk","eggs","baking powder","butter"],
//             "directions": ["In a large mixing bowl, whisk together the flour, sugar, baking powder, baking soda, and salt.","In a separate bowl, whisk the buttermilk, eggs, and melted butter until smooth.","Pour the wet ingredients into the dry mixture and gently fold until just combined. Do not overmix; some lumps are fine.","Heat a lightly buttered or oiled skillet over medium heat.","Scoop 1/4 cup of batter onto the skillet for each pancake.","Cook until bubbles form on the surface and the edges look set, about 2-3 minutes","Flip and cook the other side until golden brown, 1-2 minutes more.","Serve warm with maple syrup, fruit, or powdered sugar."],
//             "category": "breakfast",
//             "dietaryrestrictions": ["dairy", "gluten"],
//             "minutestocomplete": 25,
//             "authorid": "fce74316-e465-412b-8e57-8ff7cbd72d3d",
//             "authorname": "test_kadee",
//             "photopath": "https://www.inspiredtaste.net/wp-content/uploads/2025/07/Pancake-Recipe-1.jpg"
//     }
// ];
let recipes = [];
let idx = 0;

// rewrite this to be different
let card = document.querySelector("#recipe-info");
let startX, currX;
let dragging = false;

// more references
let titleRef = document.querySelector("#recipe-title");
let imgEl = document.querySelector("#recipe-image");
let descEl = document.querySelector("#recipe-overview");
let ingEl = document.querySelector("#recipe-ingredient-list");
let dirEl = document.querySelector("#recipe-steps-list");
let timeEl = document.querySelector("#recipe-est-time");

async function loadRecipes() {
    // const res = await fetch(API_BASE + FEED_ENDPOINT);
    // const json = await res.json();
    // recipes = json.data || [];
    // showRecipe();
    try {
        const res = await fetch(`${API_BASE}/feed/${userID}`);
        const json = await res.json();

        recipes = json.data.recipes || json.data || [];
        console.log("Recipes: ", recipes);

        if (recipes.length === 0) {
            // showEmpty();
            console.log("Recipes is of length 0.");
            return;
        }
        
        showRecipe();

    } catch (err) {
        console.error("Feed error:", err);
        // showEmpty();
    }
}

function showDefault() {
    // TODO: write something to show default and be like
    // no recipes :(
    return;
}

function showRecipe() {
    if (recipes.length === 0) return showDefault();

    const r = recipes[idx];

    console.log("we made it to showrecipes");
    console.log(r);

    titleRef.innerHTML = r.title || "Untitled Recipe";

    // display image if exists
    if (r.photopath) {
        imgEl.src = r.photopath;
        imgEl.style.display = "block";
    } else {
        imgEl.style.display = "none";
    }

    descEl.innerHTML = r.description || "(No description)";
    ingEl.innerHTML = (r.ingredients || []).join("<br>");
    dirEl.innerHTML = (r.directions || []).join("<br>");
    timeEl.innerHTML = (r.minutestocomplete  + " Minutes" || "NA");
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

