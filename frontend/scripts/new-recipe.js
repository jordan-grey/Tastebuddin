
const API_BASE = "http://localhost:5001";

async function submitRecipe(event) {
    event.preventDefault();

    const user_id = localStorage.getItem("tastebuddin_user_id");
    if (!user_id) {
        alert("You must be logged in to create a recipe.");
        return;
    }

    // Collect form values
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const category = document.getElementById("category").value.trim();
    const minutes = document.getElementById("time").value.trim();

    const ingredients = document.getElementById("ingredients").value
        .split("\n").map(s => s.trim()).filter(Boolean);

    const directions = document.getElementById("instructions").value
        .split("\n").map(s => s.trim()).filter(Boolean);

    const dietary = document.getElementById("dietary").value
        .split(",").map(s => s.trim()).filter(Boolean);

    const imageFile = document.getElementById("photo").files[0];

    // Build FormData to send to backend
    const form = new FormData();
    form.append("title", title);
    form.append("description", description);
    form.append("category", category);
    form.append("minutestocomplete", minutes);
    form.append("ingredients", JSON.stringify(ingredients));
    form.append("directions", JSON.stringify(directions));
    form.append("dietaryrestrictions", JSON.stringify(dietary));
    form.append("authorid", user_id);

    if (imageFile) {
        form.append("image", imageFile);
    }

    try {
        const res = await fetch(`${API_BASE}/recipes`, {
            method: "POST",
            body: form
        });

        const json = await res.json();
        console.log(json);

        if (!res.ok) {
            alert("Error creating recipe: " + json.error);
            return;
        }

        alert("Recipe created successfully!");
        document.getElementById("recipeForm").reset();
    } catch (err) {
        console.error(err);
        alert("Failed to submit recipe.");
    }
}

window.submitRecipe = submitRecipe;

