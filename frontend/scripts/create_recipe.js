const API = "http://localhost:5001";
const user_id = localStorage.getItem("tastebuddin_user_id");

async function submitRecipe(event) {
    event.preventDefault();

    if (!user_id) {
        alert("You must be logged in to create a recipe.");
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

    // match backend: data = request.form AND image = request.files["image"]
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

    try {
        const res = await fetch(`${API}/recipes`, {
            method: "POST",
            body: form
        });

        const json = await res.json();
        console.log("Create Recipe Response:", json);

        if (!res.ok || json.error) {
            alert("Error creating recipe: " + (json.error || res.status));
            return;
        }

        alert("Recipe created!");
        
        // Redirect to the recipe view page
        window.location.href = `recipe-view.html?recipeid=${json.recipeid}`;

    } catch (err) {
        console.error("Failed to submit recipe:", err);
        alert("Something went wrong.");
    }
}
