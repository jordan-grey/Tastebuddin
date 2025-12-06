/* 
  File: create_recipe.js
  Created By: Evan and Kadee
  Purpose:
    Handles creation and editing of user recipes. This script powers the
    "Create Recipe" page and supports both new submissions and edit mode
    (when a recipe ID is passed via ?edit=<id> in the URL).

  Main Features:
    - Detects edit mode through URL query parameter (?edit=ID).
    - Loads an existing recipe into the form for editing.
    - Collects recipe form data (title, description, ingredients, steps, dietary restrictions).
    - Handles optional image uploads through multipart FormData.
    - Submits new recipes (POST) or updates existing ones (PUT).
    - Redirects to the recipe view page upon successful submit.

  Dependencies:
    - API server at http://localhost:5001
        • GET    /recipes/<id>         → retrieve a recipe for editing
        • POST   /recipes              → create a new recipe
        • PUT    /recipes/<id>         → update an existing recipe
    - HTML page must contain input fields with IDs:
        • title, description, category, time, ingredients, instructions,
          dietary, photo, previewImage (optional for edit mode), submitBtn.
    - LocalStorage:
        • "tastebuddin_user_id" → identifies the author of the recipe.

  Key Functions:
    loadRecipeForEdit(recipeId):
        - Fetches a recipe from backend.
        - Pre-fills form with recipe data.
        - Converts array fields (ingredients, directions) to newline-separated strings.
        - Updates submit button to display “Update Recipe”.

    submitRecipe(event):
        - Prevents default form submit behavior.
        - Validates that user is logged in.
        - Collects all fields, formats arrays, builds FormData payload.
        - Sends POST (new recipe) or PUT (editing).
        - Alerts user on success or failure.
        - Redirects to the appropriate recipe view page.

  Behavior Summary:
    - On page load:
        • Checks URL for ?edit=<id>.
        • If present, script enters edit mode and loads recipe into the form.
        • If absent, page behaves as a new recipe creator.
    - Photo upload is optional; backend only updates image when included.
    - Arrays are sent as JSON strings to backend (ingredients + directions).
    - After submit, user is navigated to recipe-view.html?recipeid=<id>.

  Notes:
    - Backend must return either:
        { recipeid: <number> } on creation  
        or the full recipe object for GET requests.
    - Missing or invalid user_id will block submission.
    - Includes robust console logging for debugging.

*/

const API = "http://localhost:5001";
const user_id = localStorage.getItem("tastebuddin_user_id");

// Detect edit mode
const params = new URLSearchParams(window.location.search);
const editId = params.get("edit");
let isEditing = !!editId;

// ----------------------------
// LOAD RECIPE FOR EDIT MODE
// ----------------------------
async function loadRecipeForEdit(recipeId) {
    try {
        const res = await fetch(`${API}/recipes/${recipeId}`);
        const json = await res.json();

        if (!res.ok || json.error) {
            console.error("Error loading recipe:", json.error);
            alert("Could not load recipe.");
            return;
        }

        // Backend returns the recipe object directly
        const r = json;  
        console.log("Loaded recipe:", r);

        const ingredients = Array.isArray(r.ingredients)
            ? r.ingredients.join("\n")
            : r.ingredients || "";

        const directions = Array.isArray(r.directions)
            ? r.directions.join("\n")
            : r.directions || "";

        document.getElementById("title").value = r.title || "";
        document.getElementById("description").value = r.description || "";
        document.getElementById("category").value = r.category || "";
        document.getElementById("time").value = r.minutestocomplete || "";
        document.getElementById("ingredients").value = ingredients;
        document.getElementById("instructions").value = directions;
        document.getElementById("dietary").value = r.dietaryrestrictions || "";

        if (r.photopath) {
            document.getElementById("previewImage").src = r.photopath;
        }

        document.getElementById("submitBtn").textContent = "Update Recipe";

    } catch (err) {
        console.error("Failed to load recipe:", err);
    }
}

// -----------------------------------
// SUBMIT NEW OR UPDATED RECIPE
// -----------------------------------
async function submitRecipe(event) {
    event.preventDefault();

    if (!user_id) {
        alert("You must be logged in.");
        return;
    }

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const category = document.getElementById("category").value;
    const time = document.getElementById("time").value;
    const ingredients = document.getElementById("ingredients").value.split("\n");
    const directions = document.getElementById("instructions").value.split("\n");
    const dietary = document.getElementById("dietary").value;
    const photoFile = document.getElementById("photo").files[0];

    const form = new FormData();
    form.append("authorid", user_id);
    form.append("title", title);
    form.append("description", description);
    form.append("category", category);
    form.append("minutestocomplete", time);
    form.append("ingredients", JSON.stringify(ingredients));
    form.append("directions", JSON.stringify(directions));
    form.append("dietaryrestrictions", dietary);

    if (photoFile) {
        form.append("image", photoFile);
    }

    let url = `${API}/recipes`;
    let method = "POST";

    // EDIT MODE → send update to backend
    if (isEditing) {
        url = `${API}/recipes/${editId}`;
        method = "PUT";
    }

    try {
        const res = await fetch(url, {
            method: method,
            body: form
        });

        const json = await res.json();
        console.log("Recipe Response:", json);

        if (!res.ok || json.error) {
            alert("Error saving recipe: " + (json.error || res.status));
            return;
        }

        alert(isEditing ? "Recipe updated!" : "Recipe created!");

        const recipeId = json.recipeid || editId;

        window.location.href = `recipe-view.html?recipeid=${recipeId}`;

    } catch (err) {
        console.error("Failed to submit recipe:", err);
        alert("Something went wrong.");
    }
}

// If edit mode → load the recipe
if (isEditing) {
    loadRecipeForEdit(editId);
}
