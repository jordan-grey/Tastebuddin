from datetime import datetime, timezone
from flask import jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class RecipeService:
    def __init__(self, supabase):
        self.supabase = supabase
        self.table_name = "recipes_public"

    # -------------------
    # Utility: JSON-safe wrapper
    # -------------------
    def _json_response(self, result, status=200):
        """Helper for Flask responses."""
        if isinstance(result, dict):
            return jsonify(result), status
        return jsonify({"data": result}), status

    # -------------------
    # CRUD Operations
    # -------------------
    def get_all_recipes(self):
        try:
            response = self.supabase.table(self.table_name).select("*").execute()
            return {"data": response.data}
        except Exception as e:
            return {"error": str(e)}

    def get_recipe(self, recipe_id):
        try:
            response = self.supabase.table(self.table_name).select("*").eq("recipeid", recipe_id).execute()
            if not response.data:
                return {"error": "Recipe not found"}, 404
            return {"data": response.data}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    def create_recipe(self, data):
        try:
            data["datecreated"] = datetime.now(timezone.utc).isoformat()
            required_fields = ["title", "description", "ingredients", "directions"]
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400

            response = self.supabase.table(self.table_name).insert(data).execute()
            return {"message": "Recipe created successfully", "data": response.data}
        except Exception as e:
            return {"error": str(e)}, 500

    def update_recipe(self, recipe_id, updates):
        try:
            response = (
                self.supabase.table(self.table_name)
                .update(updates)
                .eq("recipeid", recipe_id)
                .execute()
            )
            if not response.data:
                return {"error": "Recipe not found"}, 404
            return {"message": "Recipe updated successfully", "data": response.data}
        except Exception as e:
            return {"error": str(e)}, 500

    def delete_recipe(self, recipe_id):
        try:
            response = (
                self.supabase.table(self.table_name)
                .delete()
                .eq("recipeid", recipe_id)
                .execute()
            )
            if not response.data:
                return {"error": "Recipe not found"}, 404
            return {"message": "Recipe deleted successfully"}
        except Exception as e:
            return {"error": str(e)}, 500
