const API = "http://localhost:5001";

// -------------------------------
// Get recipe ID from URL
// -------------------------------
const params = new URLSearchParams(window.location.search);
const recipeId = params.get("recipeid");

// References to DOM
const card = document.getElementById("recipe-card");
const empty = document.getElementById("no-recipes");

if (!recipeId) {
    showNotFound();
} else {
    loadRecipe(recipeId);
}

// -------------------------------
async function loadRecipe(id) {
    try {
        const res = await fetch(`${API}/recipes/${id}`);
        const json = await res.json();

        if (!res.ok || !json.data || json.data.length === 0) {
            return showNotFound();
        }

        const r = json.data[0];
        renderRecipe(r);
    } catch (err) {
        console.error(err);
        showNotFound();
    }
}

// -------------------------------
function renderRecipe(r) {
    // Ensure card visible
    card.style.display = "block";
    empty.style.display = "none";

    document.getElementById("recipe-title").innerText = r.title;
    document.getElementById("recipe-est-time").innerText =
        r.minutestocomplete ? `${r.minutestocomplete} minutes` : "N/A";
    document.getElementById("recipe-overview").innerText = r.description;

    // Image
    const img = document.getElementById("recipe-image");
    img.src = r.photopath || "default-resources/empty-dish.jpg";

    // Ingredients
    document.getElementById("recipe-ingredient-list").innerHTML =
        (r.ingredients || []).map(i => `<p>${i}</p>`).join("");

    // Directions
    document.getElementById("recipe-steps-list").innerHTML =
        (r.directions || []).map(step => `<p>${step}</p>`).join("");
}

// -------------------------------
function showNotFound() {
    card.style.display = "none";
    empty.style.display = "block";
}
