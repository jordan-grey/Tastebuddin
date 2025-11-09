from datetime import datetime
from db import supabase

# --- FILTERING HELPERS ---

def filter_recipes_by_user_restrictions(user_id: str):
    try:
        user_data = supabase.table("user_public").select("DietaryRestrictions").eq("id", user_id).execute()
        user_restrictions = user_data.data[0].get("DietaryRestrictions", [])

        recipes_data = supabase.table("recipes_public").select("*").execute()
        recipes = recipes_data.data

        # Keep recipes that have *no conflicting* restrictions
        filtered = []
        for r in recipes:
            recipe_tags = r.get("DietaryRestrictions", [])
            # If no overlap with restricted items, include it
            if not recipe_tags or any(tag in user_restrictions for tag in recipe_tags):
                filtered.append(r)

        return filtered
    except Exception as e:
        print("Error filtering recipes:", e)
        return []


def filter_users_for_new_recipe(recipe):
    """Return user_ids whose restrictions match a new recipe."""
    all_users = supabase.table("users_public").select("id, allergens").execute().data
    recipe_restrictions = recipe.get("DietaryRestrictions", [])
    suitable_users = []
    for user in all_users:
        restrictions = user.get("DietaryRestrictions", [])
        if not any(r in recipe_restrictions for r in restrictions):
            suitable_users.append(user["UserID"])
    return suitable_users


def add_to_unseen(user_ids, recipe_id):
    """Add a recipe to multiple users’ unseen feeds."""
    entries = [{"UserID": uid, "RecipeID": recipe_id, "Seen": False} for uid in user_ids]
    supabase.table("unseen_recipes").insert(entries).execute()
