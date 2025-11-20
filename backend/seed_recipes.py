# seed_recipes.py

import os
import uuid
from datetime import datetime, timezone

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in environment")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "recipe_images"
IMAGE_FOLDER = "seed_images"

# ------------------------------------------------------------------
# EXAMPLE RECIPES
# You can extend this list to 100 recipes following the same pattern.
# Each recipe has an `image_filename` that must exist in seed_images/.
# ------------------------------------------------------------------
RECIPES = [
    # --- Breakfast (sample) ---
    {
        "title": "Fluffy Buttermilk Pancakes",
        "description": "Classic fluffy pancakes perfect for a weekend breakfast.",
        "category": "breakfast",
        "ingredients": ["flour", "buttermilk", "eggs", "baking powder", "butter"],
        "directions": [
            "In a large mixing bowl, whisk together the flour, sugar, baking powder, baking soda, and salt.",
            "In a separate bowl, whisk the buttermilk, eggs, and melted butter until smooth.",
            "Pour the wet ingredients into the dry mixture and gently fold until just combined. Do not overmix; some lumps are fine.",
            "Heat a lightly buttered or oiled skillet over medium heat.",
            "Scoop 1/4 cup of batter onto the skillet for each pancake.",
            "Cook until bubbles form on the surface and the edges look set, about 2-3 minutes.",
            "Flip and cook the other side until golden brown, 1-2 minutes more.",
            "Serve warm with maple syrup, fruit, or powdered sugar."
        ],
        "dietaryrestrictions": ["dairy", "gluten"],
        "minutestocomplete": 25,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "fluffy_pancakes.jpg",
    },
    {
        "title": "Veggie Omelette",
        "description": "Egg omelette loaded with peppers, onions, and spinach.",
        "category": "breakfast",
        "ingredients": ["eggs", "bell peppers", "onion", "spinach", "cheese"],
        "directions": [
            "Dice the bell peppers, onions, and spinach. If using cheese, grate it and set aside.",
            "Heat a non-stick skillet over medium heat and drizzle with a small amount of oil.",
            "Sauté the vegetables for 3-4 minutes until softened. Transfer to a plate.",
            "In a bowl, whisk together the eggs, salt, and pepper until fully combined.",
            "Pour the eggs into the skillet and tilt the pan to spread the mixture evenly.",
            "As the eggs begin to set, gently push the edges inward with a spatula, allowing uncooked egg to flow outward.",
            "Add the sautéed vegetables (and cheese if using) to one half of the omelette.",
            "Fold the omelette in half and cook for another 1-2 minutes until fully set.",
            "Slide onto a plate and serve hot."
        ],
        "dietaryrestrictions": ["dairy"],
        "minutestocomplete": 20,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "veggie_omelette.jpg",
    },

    # --- Lunch (sample) ---
    {
        "title": "Grilled Chicken Salad",
        "description": "Light salad with grilled chicken, mixed greens, and vinaigrette.",
        "category": "lunch",
        "ingredients": ["chicken breast", "mixed greens", "tomatoes", "vinaigrette"],
        "directions": [
            "Season the chicken breast on both sides with salt, pepper, and a drizzle of olive oil.",
            "Heat a grill pan or outdoor grill over medium-high heat.",
            "Cook the chicken for 5-7 minutes per side, or until the internal temperature reaches 165°F (74°C).",
            "Let the chicken rest for 5 minutes, then slice thinly.",
            "Rinse and dry the mixed greens, then place them in a large serving bowl.",
            "Add sliced tomatoes, cucumbers, or any additional vegetables you prefer.",
            "Top the salad with the sliced chicken.",
            "Drizzle with vinaigrette and toss gently before serving."
        ],
        "dietaryrestrictions": [],
        "minutestocomplete": 30,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "grilled_chicken_salad.jpg",
    },
    {
        "title": "Caprese Sandwich",
        "description": "Mozzarella, tomato, and basil on toasted ciabatta.",
        "category": "lunch",
        "ingredients": ["ciabatta", "mozzarella", "tomato", "basil", "olive oil"],
        "directions": [
            "Slice the ciabatta roll in half and lightly drizzle each side with olive oil.",
            "Layer fresh mozzarella slices evenly across the bottom half of the bread.",
            "Add tomato slices on top of the cheese, followed by fresh basil leaves.",
            "Sprinkle with a pinch of salt and black pepper.",
            "Close the sandwich, pressing gently.",
            "Optional: Toast the sandwich on a panini press or skillet for 2-3 minutes until warm and lightly crisp.",
            "Slice in half and serve immediately."
        ],
        "dietaryrestrictions": ["dairy", "gluten", "vegetarian"],
        "minutestocomplete": 15,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "caprese_sandwich.jpg",
    },

    # --- Dinner (sample) ---
    {
        "title": "Lemon Garlic Salmon",
        "description": "Baked salmon fillets with lemon, garlic, and herbs.",
        "category": "dinner",
        "ingredients": ["salmon", "lemon", "garlic", "olive oil", "parsley"],
        "directions": [
            "Preheat the oven to 400°F (205°C). Line a baking sheet with foil.",
            "Place the salmon fillets on the sheet and pat dry with a paper towel.",
            "In a small bowl, combine minced garlic, olive oil, lemon juice, salt, and pepper.",
            "Brush the mixture evenly over the salmon.",
            "Lay lemon slices over the fillets and sprinkle with fresh parsley.",
            "Bake for 12-15 minutes, or until the salmon flakes easily with a fork.",
            "Remove from the oven and serve warm with an extra squeeze of lemon."
        ],
        "dietaryrestrictions": ["fish"],
        "minutestocomplete": 30,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "lemon_garlic_salmon.jpg",
    },
    {
        "title": "Creamy Tomato Pasta",
        "description": "Pasta in a creamy tomato sauce with parmesan.",
        "category": "dinner",
        "ingredients": ["pasta", "tomato sauce", "cream", "parmesan", "garlic"],
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
        "dietaryrestrictions": ["dairy", "gluten"],
        "minutestocomplete": 25,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "creamy_tomato_pasta.jpg",
    },

    # --- Dessert (sample) ---
    {
        "title": "Chocolate Fudge Brownies",
        "description": "Rich, fudgy brownies with crackly tops.",
        "category": "dessert",
        "ingredients": ["flour", "cocoa powder", "butter", "sugar", "eggs"],
        "directions": [
            "Preheat oven to 350°F (175°C). Grease an 8x8-inch baking pan or line with parchment paper.",
            "In a saucepan, melt butter and cocoa powder together over low heat, stirring until smooth.",
            "Remove from heat and whisk in sugar until well combined.",
            "Stir in eggs one at a time, mixing thoroughly after each addition.",
            "Fold in flour and salt, mixing only until incorporated—do not overmix.",
            "Pour the batter into the prepared pan and smooth the top.",
            "Bake for 22-28 minutes, or until a toothpick inserted in the center comes out with moist crumbs.",
            "Cool completely before slicing for clean edges."
        ],
        "dietaryrestrictions": ["dairy", "gluten"],
        "minutestocomplete": 45,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "chocolate_fudge_brownies.jpg",
    },
    {
        "title": "Classic Cheesecake",
        "description": "Creamy baked cheesecake on a graham cracker crust.",
        "category": "dessert",
        "ingredients": ["cream cheese", "sugar", "eggs", "graham crackers", "butter"],
        "directions": [
            "Preheat oven to 325°F (165°C). Wrap the outside of a springform pan with foil.",
            "Crush graham crackers and mix with melted butter and sugar to form a crust.",
            "Press the mixture firmly into the bottom of the pan.",
            "In a large bowl, beat softened cream cheese until smooth.",
            "Add sugar, sour cream, and vanilla; beat until fully incorporated.",
            "Mix in eggs one at a time, blending gently to avoid overmixing.",
            "Pour the filling into the crust.",
            "Place the pan in a water bath and bake for 60-75 minutes until the center jiggles slightly.",
            "Turn off oven and let cheesecake cool inside with the door cracked for 1 hour.",
            "Chill for at least 4 hours before serving."
        ],
        "dietaryrestrictions": ["dairy", "gluten"],
        "minutestocomplete": 90,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "classic_cheesecake.jpg",
    },

    # --- Vegan (sample) ---
    {
        "title": "Vegan Buddha Bowl",
        "description": "Quinoa bowl with roasted veggies, chickpeas, and tahini sauce.",
        "category": "vegan",
        "ingredients": ["quinoa", "chickpeas", "sweet potato", "broccoli", "tahini"],
        "directions": [
            "Preheat oven to 400°F (205°C). Chop sweet potatoes and broccoli into bite-sized pieces.",
            "Toss vegetables with olive oil, salt, and pepper, then spread onto a baking sheet.",
            "Roast for 20-25 minutes, flipping halfway through.",
            "Meanwhile, cook quinoa according to package instructions.",
            "Drain and rinse chickpeas, then season with paprika, salt, and garlic powder.",
            "Assemble the bowl: quinoa on the bottom, topped with roasted vegetables and chickpeas.",
            "Whisk together tahini, lemon juice, and water to make a drizzleable sauce.",
            "Pour sauce over the bowl and serve warm."
        ],
        "dietaryrestrictions": ["vegan", "vegetarian"],
        "minutestocomplete": 40,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "vegan_buddha_bowl.jpg",
    },
    {
        "title": "Lentil Curry",
        "description": "Hearty vegan lentil curry with coconut milk.",
        "category": "vegan",
        "ingredients": ["lentils", "coconut milk", "onion", "garlic", "curry powder"],
        "directions": [
            "Rinse the lentils thoroughly under running water.",
            "Heat oil in a pot and sauté chopped onion, garlic, and ginger for 3-4 minutes.",
            "Stir in curry powder and toast briefly until fragrant.",
            "Add lentils, vegetable broth, and coconut milk.",
            "Bring to a simmer, then reduce heat and cook for 20-25 minutes until lentils are tender.",
            "Season with salt, pepper, and lime juice.",
            "Serve over rice or with warm naan."
        ],
        "dietaryrestrictions": ["vegan", "vegetarian"],
        "minutestocomplete": 50,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "lentil_curry.jpg",
    },

    # --- Snacks (sample) ---
    {
        "title": "Peanut Butter Energy Bites",
        "description": "No-bake oats and peanut butter snack balls.",
        "category": "snack",
        "ingredients": ["oats", "peanut butter", "honey", "chia seeds"],
        "directions": [
            "In a mixing bowl, combine oats, peanut butter, honey, and chia seeds.",
            "Stir until all ingredients are evenly incorporated.",
            "If mixture feels too dry, add a teaspoon of water; if too sticky, add a bit more oats.",
            "Scoop tablespoon-sized portions and roll into balls.",
            "Place on a plate and chill in the refrigerator for at least 20 minutes.",
            "Store in an airtight container for up to one week."
        ],
        "dietaryrestrictions": ["peanuts", "gluten"],
        "minutestocomplete": 15,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "peanut_butter_energy_bites.jpg",
    },
    {
        "title": "Veggie Hummus Platter",
        "description": "Fresh veggies served with creamy hummus.",
        "category": "snack",
        "ingredients": ["carrots", "cucumber", "bell peppers", "hummus"],
        "directions": [
            "Wash and slice vegetables into uniform sticks or bite-sized pieces.",
            "Arrange carrots, cucumbers, and bell peppers neatly on a serving plate.",
            "Spoon hummus into a bowl and drizzle with olive oil and paprika if desired.",
            "Place the hummus bowl in the center of the platter.",
            "Serve immediately or refrigerate until ready to enjoy."
        ],
        "dietaryrestrictions": ["vegan", "vegetarian"],
        "minutestocomplete": 10,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "veggie_hummus_platter.jpg",
    },

    # --- Drinks (sample) ---
    {
        "title": "Iced Matcha Latte",
        "description": "Refreshing iced matcha latte with oat milk.",
        "category": "drink",
        "ingredients": ["matcha powder", "oat milk", "ice", "sweetener"],
       "directions": [
            "In a small bowl, sift matcha powder to remove any clumps.",
            "Add 2-3 tablespoons of warm water and whisk vigorously in a zig-zag motion until frothy.",
            "Fill a glass with ice cubes.",
            "Pour oat milk over the ice.",
            "Slowly pour the matcha mixture on top to create a layered effect.",
            "Sweeten to taste and stir before drinking."
        ],
        "dietaryrestrictions": ["vegan", "vegetarian"],
        "minutestocomplete": 5,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "iced_matcha_latte.jpg",
    },
    {
        "title": "Strawberry Smoothie",
        "description": "Fruit smoothie with strawberries, banana, and yogurt.",
        "category": "drink",
        "ingredients": ["strawberries", "banana", "yogurt", "milk"],
        "directions": [
            "Wash and hull the strawberries.",
            "Add strawberries, banana, yogurt, and milk to a blender.",
            "Blend on high until completely smooth.",
            "Taste and add honey or extra milk as needed to adjust sweetness and thickness.",
            "Pour into a chilled glass and serve immediately."
        ],
        "dietaryrestrictions": ["dairy"],
        "minutestocomplete": 5,
        "authorid": "07989fc3-19cc-4478-b814-122510715767",  # test_kadee
        "authorname": "test_user",
        "image_filename": "strawberry_smoothie.jpg",
    },
]


def upload_image(filename: str) -> str:
    """Upload a local file from seed_images/ and return its public URL."""
    path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(path):
        print(f"[WARN] Image file not found: {path}. Skipping image upload.")
        return None

    with open(path, "rb") as f:
        file_bytes = f.read()

    storage_name = f"{uuid.uuid4()}_{filename}"
    print(f"[IMG] Uploading {filename} as {storage_name} to bucket {BUCKET_NAME}")

    res = supabase.storage.from_(BUCKET_NAME).upload(storage_name, file_bytes)
    # Supabase Python client returns None or raises on error; being defensive:
    if isinstance(res, dict) and res.get("error"):
        raise Exception(res["error"]["message"])

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_name)
    print(f"[IMG] -> Public URL: {public_url}")
    return public_url


def seed():
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    for idx, recipe in enumerate(RECIPES, start=1):
        print(f"\n[SEED] Inserting recipe {idx}/{len(RECIPES)}: {recipe['title']}")
        recipe_data = dict(recipe)  # shallow copy

        image_filename = recipe_data.pop("image_filename", None)
        photopath = None

        if image_filename:
            try:
                photopath = upload_image(image_filename)
            except Exception as e:
                print(f"[ERROR] Could not upload image {image_filename}: {e}")

        if photopath:
            recipe_data["photopath"] = photopath

        # add timestamp if desired
        recipe_data.setdefault("datecreated", datetime.now(timezone.utc).isoformat())

        resp = supabase.table("recipes_public").insert(recipe_data).execute()
        print(f"[DB] Inserted recipe id(s): {[r.get('recipeid') for r in resp.data]}")


if __name__ == "__main__":
    seed()
