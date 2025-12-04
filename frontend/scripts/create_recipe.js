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
