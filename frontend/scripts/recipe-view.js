const API_BASE = "http://localhost:5001";


data = [
    {
        "authorid": "07989fc3-19cc-4478-b814-122510715767",
        "authorname": "test_user",
        "category": "dinner",
        "datecreated": "2025-11-19T00:56:50.301391+00:00",
        "description": "Pasta in a creamy tomato sauce with parmesan.",
        "dietaryrestrictions": [
            "dairy",
            "gluten"
        ],
        "directions": [
            "Bring a large pot of salted water to a boil and cook the pasta according to package instructions. Reserve 1/2 cup of pasta water.",
            "In a saucepan, heat olive oil over medium heat and sauté minced garlic until fragrant, about 1 minute.",
            "Stir in the tomato sauce and let it simmer for 3-4 minutes.",
            "Add the heavy cream and stir until the sauce turns a light orange color.",
            "Sprinkle in Parmesan and stir until melted and smooth.",
            "Fold in the cooked pasta, adding a splash of reserved pasta water if needed to loosen.",
            "Season with salt, pepper, and Italian herbs to taste.",
            "Serve warm with extra Parmesan on top."
        ],
        "ingredients": [
            "pasta",
            "tomato sauce",
            "cream",
            "parmesan",
            "garlic"
        ],
        "likes": 1,
        "minutestocomplete": 25,
        "photopath": "https://nxzaxhgyzapnnqcfjxpn.supabase.co/storage/v1/object/public/recipe_images/693a084f-4932-45eb-96bc-3628ba35029e_creamy_tomato_pasta.jpg",
        "recipeid": 60,
        "title": "Creamy Tomato Pasta"
    }
]

const params = new URLSearchParams(window.location.search);
const id = params.get("recipeid");

fetch(`${API_BASE}/recipes/${id}`)
    .then(res => res.json())
    .then(data => {
        console.log("User feed: ", data);
        renderRecipe(data.data);
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
