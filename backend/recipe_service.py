from datetime import datetime, timezone
from flask import jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class RecipeService:
    def __init__(self, supabase):
        self.supabase = supabase
        self.table_name = "recipes_public"
        self.bucket = "recipe_images"

    # ------------------------------------------------------
    # IMAGE UPLOAD
    # ------------------------------------------------------
    def upload_image(self, image_file, recipe_id=None):
        """
        Uploads an image to Supabase Storage and returns the public URL.
        """
        ext = image_file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        # Store inside a recipe folder: images/recipes/<id>/<filename>
        folder = f"images/recipes/{recipe_id or 'unassigned'}"
        full_path = f"{folder}/{filename}"

        res = self.supabase.storage.from_(self.bucket).upload(
            full_path,
            image_file.read(),
        )

        if "error" in str(res).lower():
            raise Exception("Failed to upload image")

        return self.supabase.storage.from_(self.bucket).get_public_url(full_path)

    # ------------------------------------------------------
    # CLEANUP HELPERS
    # ------------------------------------------------------
    def delete_image_at_path(self, path: str):
        """Delete a single file from Supabase Storage."""
        if not path:
            return
        try:
            self.supabase.storage.from_(self.bucket).remove([path])
            print(f"[CLEANUP] Deleted image: {path}")
        except Exception as e:
            print(f"[CLEANUP ERROR] {e}")

    def delete_all_images_for_recipe(self, recipe_id: int):
        """Deletes all images stored under images/recipes/<recipeid>/"""
        folder = f"images/recipes/{recipe_id}"

        try:
            files = self.supabase.storage.from_(self.bucket).list(folder)
            if not files:
                return

            paths = [f"{folder}/{f['name']}" for f in files]
            self.supabase.storage.from_(self.bucket).remove(paths)
            print(f"[CLEANUP] Deleted {len(paths)} images for recipe {recipe_id}")
        except Exception as e:
            print(f"[CLEANUP ERROR] Could not delete folder {folder}: {e}")

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------
    def get_all_recipes(self):
        try:
            response = self.supabase.table(self.table_name).select("*").execute()
            return {"data": response.data}
        except Exception as e:
            return {"error": str(e)}

    def get_recipe(self, recipe_id):
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("recipeid", recipe_id)
                .execute()
            )
            if not response.data:
                return {"error": "Recipe not found"}, 404
            return {"data": response.data}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def create_recipe(self, data, image_file=None):
        try:
            data["datecreated"] = datetime.now(timezone.utc).isoformat()

            required = ["title", "description", "ingredients", "directions", "authorid"]
            for field in required:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400

            # First create recipe WITHOUT image
            response = self.supabase.table(self.table_name).insert(data).execute()
            recipe = response.data[0]
            recipe_id = recipe["recipeid"]

            # If image exists → upload + update recipe
            if image_file:
                url = self.upload_image(image_file, recipe_id)
                self.supabase.table(self.table_name).update(
                    {"photopath": url}
                ).eq("recipeid", recipe_id).execute()
                recipe["photopath"] = url

            return {"message": "Recipe created successfully", "data": [recipe]}
        except Exception as e:
            return {"error": str(e)}, 500

    def update_recipe(self, recipe_id, updates, image_file=None):
        try:
            if image_file:
                url = self.upload_image(image_file, recipe_id)
                updates["photopath"] = url

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
            self.delete_all_images_for_recipe(recipe_id)

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
