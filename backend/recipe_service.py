# recipe_service.py
from flask import jsonify
from datetime import datetime, timezone
from db import supabase
from recipe_utility import (
    filter_recipes_by_user_restrictions,
    filter_users_for_new_recipe,
    add_to_unseen
)
import traceback

# ---------- CRUD Functions for Recipes ---------- #

def get_all_recipes():
    try:
        response = supabase.table("recipes_public").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_recipe_by_id(recipe_id):
    try:
        response = supabase.table("recipes_public").select("*").eq("recipe_id", recipe_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- CREATE RECIPE ---

'''
def create_recipe(data):
    try:
        data["DateCreated"] = datetime.now(timezone.utc).isoformat()
        required_fields = ["Title", "Description", "Ingredients", "Directions"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Save recipe
        response = supabase.table("recipes_public").insert(data).execute()
        recipe_id = response.data[0]["RecipeID"]

        # Get users who can see this recipe (filter against user restrictions)
        users_to_notify = filter_users_for_new_recipe(data)
        add_to_unseen(users_to_notify, recipe_id)

        return jsonify({"message": "Recipe created successfully", "data": response.data}), 201

    except Exception as e:
        print("Error in create_recipe:", e)
        return jsonify({"error": str(e)}), 500
    '''
def create_recipe(data):
    try:
        data["DateCreated"] = datetime.now(timezone.utc).isoformat()
        required_fields = ["title", "description", "ingredients", "directions"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        print("📦 Incoming recipe data:", data)  # Debug line

        data = {
            "title": data.get("Title"),
            "description": data.get("Description"),
            "ingredients": data.get("Ingredients"),
            "directions": data.get("Directions"),
            "category": data.get("Category"),
            "dietaryrestrictions": data.get("DietaryRestrictions"),
            "minutestocomplete": data.get("MinutesToComplete"),
            "photopath": data.get("PhotoPath"),
            "authorid": data.get("AuthorID"),
            "authorname": data.get("AuthorName"),
            "datecreated": datetime.now(timezone.utc).isoformat()
        }
                
        response = supabase.table("recipes_public").insert(data).execute()
        print("Supabase insert response:", response)  # Debug line

        return jsonify({"message": "Recipe created successfully", "data": response.data}), 201
    except Exception as e:
        print("Error in create_recipe:", str(e))
        print(traceback.format_exc())  # Shows full error in console
        return jsonify({"error": str(e)}), 500

# --- ONBOARDING USER ---
def onboard_new_user(user_id):
    try:
        filtered_recipes = filter_recipes_by_user_restrictions(user_id)
        if not filtered_recipes:
            return jsonify({"message": "No matching recipes found for user."}), 200

        # Add to unseen
        entries = [{"UserID": user_id, "RecipeID": r["RecipeID"], "Seen": False} for r in filtered_recipes]
        supabase.table("UnseenRecipes").insert(entries).execute()
        return jsonify({"message": f"{len(filtered_recipes)} recipes added to unseen feed."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_recipe(recipe_id, data):
    try:
        response = supabase.table("recipes_public").update(data).eq("recipeid", recipe_id).execute()
        if response.data:
            return jsonify({"message": "Recipe updated successfully", "data": response.data}), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_recipe(recipe_id):
    try:
        response = supabase.table("recipes_public").delete().eq("recipeid", recipe_id).execute()
        return jsonify({"message": "Recipe deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
