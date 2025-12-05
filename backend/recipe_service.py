
"""
===============================================================
 File: recipe_service.py
 System: Tastebuddin — Recipe Discovery & Social Cooking App
 Created: 2024-11-01
 Authors: Kadee Wheeler

 Description:
     This file defines the RecipeService class, which handles all
     database operations related to user recipes — including CRUD
     operations, image uploads, storage management, and automatic
     updates to user feed data (unseen recipe lists).

     This module is part of the Tastebuddin backend and is used by
     app.py to serve REST API endpoints.

===============================================================
"""

# -----------------------------
# Imports & Environment Setup
# -----------------------------
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


# ===============================================================
# CLASS: RecipeService
# Handles all recipe CRUD + image storage + helper logic.
# ===============================================================
class RecipeService:
    """
    Service class for creating, retrieving, updating, and deleting
    recipes in the Tastebuddin application.

    Attributes:
        supabase (Client): Supabase database client instance.
        table_name (str): Name of the Supabase table storing recipes.
        bucket (str): Name of the Supabase Storage bucket for images.
    """

    def __init__(self, supabase):
        """Initialize service with Supabase client."""
        self.supabase = supabase
        self.table_name = "recipes_public"
        self.bucket = "recipe_images"

    # ===========================================================
    # IMAGE UPLOAD FUNCTIONS
    # ===========================================================

    def upload_image(self, image_file, recipe_id=None):
        """
        Upload an image to Supabase Storage and return its public URL.

        Args:
            image_file (FileStorage): Raw uploaded image.
            recipe_id (int | None): If known, image saved under this folder.

        Returns:
            str: Publicly accessible URL of the uploaded image.

        Raises:
            Exception: If upload fails.
        """
        ext = image_file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        folder = f"images/recipes/{recipe_id or 'unassigned'}"
        full_path = f"{folder}/{filename}"

        res = self.supabase.storage.from_(self.bucket).upload(
            full_path,
            image_file.read(),
        )

        if "error" in str(res).lower():
            raise Exception("Failed to upload image")

        return self.supabase.storage.from_(self.bucket).get_public_url(full_path)

    # -----------------------------------------------------------

    def delete_image_at_path(self, path):
        """
        Delete a single image file from Supabase Storage.

        Args:
            path (str): File path inside storage bucket.
        """
        if not path:
            return
        try:
            self.supabase.storage.from_(self.bucket).remove([path])
            print(f"[CLEANUP] Deleted {path}")
        except Exception as e:
            print("[CLEANUP ERROR]", e)

    # -----------------------------------------------------------

    def delete_all_images_for_recipe(self, recipe_id):
        """
        Delete all images stored inside a recipe folder.

        Args:
            recipe_id (int): Recipe identifier.
        """
        folder = f"images/recipes/{recipe_id}"

        try:
            files = self.supabase.storage.from_(self.bucket).list(folder)
            if not files:
                return

            paths = [f"{folder}/{f['name']}" for f in files]
            self.supabase.storage.from_(self.bucket).remove(paths)
            print(f"[CLEANUP] Deleted {len(paths)} images for recipe {recipe_id}")

        except Exception as e:
            print("[CLEANUP ERROR]", e)

    # ===========================================================
    # CRUD FUNCTIONS
    # ===========================================================

    def get_all_recipes(self):
        """
        Fetch all recipes from the database.

        Returns:
            dict: { data: [...] } on success or { error: "..."} on failure.
        """
        try:
            response = self.supabase.table(self.table_name).select("*").execute()
            return {"data": response.data}
        except Exception as e:
            return {"error": str(e)}

    # -----------------------------------------------------------
        
    def get_recipe(self, recipe_id):
        """
            Fetch a single recipe by ID.

            Args:
                recipe_id (int): Recipe identifier.

            Returns:
                tuple(dict, int): Response JSON + HTTP status.
        """
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("recipeid", recipe_id)
                .execute()
            )

            if not response.data:
                return {"error": "Recipe not found"}, 404

            # Consistent with all other endpoints
            return {"data": response.data[0]}, 200

        except Exception as e:
            return {"error": str(e)}, 500


    # -----------------------------------------------------------

    def create_recipe(self, data, image_file=None):
        """
        Create a new recipe, update user unseen feeds, and optionally
        upload image to storage.

        Args:
            data (dict): Raw form fields from the client.
            image_file (FileStorage | None): Uploaded file.

        Returns:
            tuple(dict, int): JSON response + status code.
        """
        try:
            # Add timestamp
            data["datecreated"] = datetime.now(timezone.utc).isoformat()

            # Required fields check
            required = ["title", "description", "ingredients", "directions", "authorid"]
            for field in required:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400

            # Lookup author_name from users_public
            lookup = (
                self.supabase.table("users_public")
                .select("username")
                .eq("id", data["authorid"])
                .execute()
            )
            if not lookup.data:
                return {"error": "Invalid authorid"}, 400

            data["authorname"] = lookup.data[0]["username"]

            # Convert list-like fields
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

            # Insert recipe WITHOUT image first
            response = self.supabase.table(self.table_name).insert(data).execute()
            recipe = response.data[0]
            recipe_id = recipe["recipeid"]

            # ------------------------------------------------------
            # Update user unseen recipe feeds
            # ------------------------------------------------------
            try:
                all_users = (
                    self.supabase.table("users_public")
                    .select("*")
                    .execute()
                ).data or []

                allergens = recipe.get("dietaryrestrictions", [])

                for user in all_users:
                    user_allergens = user.get("allergens", []) or []
                    if any(a in allergens for a in user_allergens):
                        continue  # Skip unsafe recipes

                    unseen = user.get("unseen_recipes", []) or []
                    if recipe_id not in unseen:
                        unseen.append(recipe_id)
                        self.supabase.table("users_public") \
                            .update({"unseen_recipes": unseen}) \
                            .eq("id", user["id"]) \
                            .execute()

            except Exception as e:
                print("[WARN] Failed unseen-update:", e)

            # ------------------------------------------------------
            # Upload IMAGE after row exists
            # ------------------------------------------------------
            if image_file:
                url = self.upload_image(image_file, recipe_id)
                self.supabase.table(self.table_name) \
                    .update({"photopath": url}) \
                    .eq("recipeid", recipe_id) \
                    .execute()
                recipe["photopath"] = url

            return {
                "message": "Recipe created successfully",
                "recipeid": recipe_id,
                "data": recipe
            }, 201

        except Exception as e:
            return {"error": str(e)}, 500

    # -----------------------------------------------------------

    def update_recipe(self, recipe_id, updates, image_file=None):
        """
        Basic update for general fields (without permission control).

        Args:
            recipe_id (int)
            updates (dict)
            image_file (FileStorage | None)

        Returns:
            dict or tuple: update response.
        """
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

            return {
                "message": "Recipe updated successfully",
                "data": response.data
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500

    # -----------------------------------------------------------

    def delete_recipe(self, recipe_id):
        """
        Delete a recipe and all associated images.

        Args:
            recipe_id (int)

        Returns:
            dict: Success or error message.
        """
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

    # -----------------------------------------------------------

    def edit_recipe(self, recipe_id, author_id, updates, image_file=None):
        """
        Safe update for an existing recipe. Only the author may edit.

        Args:
            recipe_id (int)
            author_id (str)
            updates (dict)
            image_file (FileStorage | None)

        Returns:
            tuple(dict, int): Response + HTTP status.
        """
        try:
            # 1) Fetch recipe
            res = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("recipeid", recipe_id)
                .execute()
            )
            if not res.data:
                return {"error": "Recipe not found"}, 404

            recipe = res.data[0]

            # 2) Permission check
            if recipe["authorid"] != author_id:
                return {"error": "Unauthorized"}, 403

            # 3) Parse list fields
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
                val = parse_list(field)
                if val is not None:
                    parsed[field] = val

            # Add simple text fields
            for field in ["title", "description", "category", "minutestocomplete"]:
                if field in updates:
                    parsed[field] = updates[field]

            # 4) Replace image if provided
            if image_file:
                self.delete_all_images_for_recipe(recipe_id)
                url = self.upload_image(image_file, recipe_id)
                parsed["photopath"] = url

            # 5) Update row
            response = (
                self.supabase.table(self.table_name)
                .update(parsed)
                .eq("recipeid", recipe_id)
                .execute()
            )

            return {"message": "Recipe updated successfully", "data": response.data}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    # -----------------------------------------------------------

    def get_recipes_by_author(self, authorid):
        """
        Fetch all recipes created by one user.

        Args:
            authorid (str): UUID of author.

        Returns:
            list: Recipe rows or empty list.
        """
        res = (
            self.supabase
                .table(self.table_name)
                .select("*")
                .eq("authorid", authorid)
                .execute()
        )
        return res.data or []
