# recipe_service.py
from flask import jsonify
from datetime import datetime
from db import supabase

# ---------- CRUD Functions for Recipes ---------- #

def get_all_recipes():
    try:
        response = supabase.table("recipes").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_recipe_by_id(recipe_id):
    try:
        response = supabase.table("recipes").select("*").eq("recipe_id", recipe_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_recipe(data):
    try:
        # Add timestamp and validation
        data["DateCreated"] = datetime.utcnow().isoformat()
        required_fields = ["Title", "Description", "Ingredients", "Directions"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        response = supabase.table("recipes").insert(data).execute()
        return jsonify({"message": "Recipe created successfully", "data": response.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_recipe(recipe_id, data):
    try:
        response = supabase.table("recipes").update(data).eq("recipe_id", recipe_id).execute()
        if response.data:
            return jsonify({"message": "Recipe updated successfully", "data": response.data}), 200
        else:
            return jsonify({"message": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_recipe(recipe_id):
    try:
        response = supabase.table("recipes").delete().eq("recipe_id", recipe_id).execute()
        return jsonify({"message": "Recipe deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
