from datetime import datetime, timezone
from flask import jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import uuid
import json 


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
                

            def parse_list(field):
                        raw = data.get(field, "[]")
                        if isinstance(raw, list):
                            return raw
                        try:
                            return json.loads(raw)
                        except:
                            return []

            data["ingredients"] = parse_list("ingredients")
            data["directions"] = parse_list("directions")
            data["dietaryrestrictions"] = parse_list("dietaryrestrictions")

            # First create recipe WITHOUT image
            response = self.supabase.table(self.table_name).insert(data).execute()
            recipe = response.data[0]
            recipe_id = recipe["recipeid"]

            try:
                # Get all users
                users_res = self.supabase.table("users_public").select("*").execute()
                users = users_res.data or []

                # Get allergens from the recipe
                recipe_allergens = recipe.get("dietaryrestrictions", []) or []
                if isinstance(recipe_allergens, str):
                    recipe_allergens = [recipe_allergens]

                for user in users:
                    user_id = user["id"]
                    user_allergens = user.get("allergens", []) or []

                    # skip if recipe conflicts with user allergens
                    if any(a in recipe_allergens for a in user_allergens):
                        continue

                    unseen = user.get("unseen_recipes", []) or []

                    # Add if not already there
                    if recipe_id not in unseen:
                        unseen.append(recipe_id)

                        self.supabase.table("users_public") \
                            .update({"unseen_recipes": unseen}) \
                            .eq("id", user_id) \
                            .execute()

            except Exception as e:
                print("[WARN] Failed updating user unseen_recipes:", e)

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

    def edit_recipe(self, recipe_id, author_id, updates, image_file=None):
        """
        Safely update a recipe ONLY if the requester is the author.
        Includes list parsing and optional image replacement.
        """

        try:
            # 1. Fetch recipe
            res = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("recipeid", recipe_id)
                .execute()
            )
            if not res.data:
                return {"error": "Recipe not found"}, 404

            recipe = res.data[0]

            # 2. Permission check
            if recipe["authorid"] != author_id:
                return {"error": "Unauthorized: only the author can edit this recipe"}, 403

            # 3. Parse list-like fields
            def parse_list(field):
                raw = updates.get(field)
                if raw is None:
                    return None
                if isinstance(raw, list):
                    return raw
                try:
                    return json.loads(raw)
                except:
                    return []

            parsed = {}
            for field in ["ingredients", "directions", "dietaryrestrictions"]:
                parsed_list = parse_list(field)
                if parsed_list is not None:
                    parsed[field] = parsed_list

            # Add the simple fields (title, description, category, minutes)
            for field in ["title", "description", "category", "minutestocomplete"]:
                if field in updates:
                    parsed[field] = updates[field]

            # 4. Handle optional image upload
            if image_file:
                # Delete old images first
                self.delete_all_images_for_recipe(recipe_id)

                url = self.upload_image(image_file, recipe_id)
                parsed["photopath"] = url

            # 5. Perform update
            response = (
                self.supabase.table(self.table_name)
                .update(parsed)
                .eq("recipeid", recipe_id)
                .execute()
            )

            return {
                "message": "Recipe updated successfully",
                "data": response.data
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500

