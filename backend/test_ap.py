"""
Purpose: Integration tests verifying interaction between RecipeService and a
         real Supabase backend. Ensures creation, updating, deletion, and image
         upload behavior work as expected.
Created: December 2024
Authors: Kadee Wheeler

Part of System:
    This is part of the automated testing suite for the Tastebuddin backend.
    These tests use a real Supabase instance and Auth user to confirm correct
    behavior of RecipeService under production-like conditions.

Modifications:
    - Documentation added (2025-12-04)
"""




import unittest
from recipe_service import RecipeService
from supabase import create_client
import os
import io

class RecipeServiceDatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load service key (must be SERVICE ROLE key!)
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        cls.supabase = create_client(url, key)

        cls.service = RecipeService(cls.supabase)

        # ---- Create REAL Auth user ----
        auth_user = cls.supabase.auth.admin.create_user({
            "email": "unit_test3xs@example.com",
            "password": "test-password-123",
            "email_confirm": True
        })

        cls.test_user_id = auth_user.user.id

        # ---- Insert into users_public ----
        cls.supabase.table("users_public").upsert({
            "id": cls.test_user_id,
            "username": "unit_test_user",
            "liked_recipes": [],
            "disliked_recipes": [],
            "unseen_recipes": [],
            "allergens": [],
            "total_likes": 0
        }).execute()

        # ---- Create a base recipe for tests ----
        base_recipe = {
            "title": "BASE Brownie",
            "description": "Test base recipe",
            "ingredients": ["sugar"],
            "directions": ["bake"],
            "category": "dessert",
            "dietaryrestrictions": ["vegetarian"],
            "minutestocomplete": 5,
            "authorid": cls.test_user_id,
            "authorname": "unit_test_user",
        }

        created = cls.service.create_recipe(base_recipe)
        if "data" not in created:
            raise RuntimeError(f"Failed to create base recipe: {created}")

        cls.base_recipe_id = created["data"][0]["recipeid"]

    # ---------- TESTS ----------

    def test_1_create_recipe(self):
        data = {
            "title": "UnitTest Brownie",
            "description": "A chocolate brownie created by tests.",
            "ingredients": ["flour", "sugar", "cocoa"],
            "directions": ["mix", "bake"],
            "category": "dessert",
            "dietaryrestrictions": ["vegetarian"],
            "minutestocomplete": 30,
            "authorid": self.test_user_id,
            "authorname": "unit_test_user"
        }

        result = self.service.create_recipe(data)
        self.assertIn("data", result)

    def test_2_get_all_recipes(self):
        result = self.service.get_all_recipes()
        self.assertIn("data", result)

    def test_3_get_single_recipe(self):
        result, status = self.service.get_recipe(self.base_recipe_id)
        self.assertEqual(status, 200)
        self.assertIn("data", result)

    def test_4_update_recipe(self):
        update_data = {"description": "Updated via unit test!"}
        result = self.service.update_recipe(self.base_recipe_id, update_data)
        self.assertIn("data", result)

    def test_5_delete_recipe(self):
        """Create → Delete → Confirm"""
        temp_recipe = {
            "title": "DeleteMe",
            "description": "Temp record",
            "ingredients": ["flour"],
            "directions": ["mix"],
            "dietaryrestrictions": ["vegetarian"],
            "category": "dessert",
            "authorid": self.test_user_id,
            "authorname": "unit_test_user",
            "minutestocomplete": 10,
        }

        created = self.service.create_recipe(temp_recipe)
        self.assertIn("data", created)
        recipe_id = created["data"][0]["recipeid"]

        delete_resp = self.service.delete_recipe(recipe_id)
        self.assertEqual(delete_resp["message"], "Recipe deleted successfully")

        confirm_resp, status = self.service.get_recipe(recipe_id)
        self.assertEqual(status, 404)
        self.assertIn("error", confirm_resp)

    def test_6_create_recipe_with_image(self):
        fake_img_bytes = io.BytesIO(b"fake image bytes")

        class FakeFile:
            def __init__(self, f, name):
                self.fileobj = f
                self.filename = name
            def read(self):
                return self.fileobj.read()

        img = FakeFile(fake_img_bytes, "test.jpg")

        data = {
            "title": "ImageTest",
            "description": "Testing image upload",
            "ingredients": ["flour"],
            "directions": ["mix"],
            "category": "dessert",
            "dietaryrestrictions": ["vegetarian"],
            "minutestocomplete": 10,
            "authorid": self.test_user_id,
            "authorname": "unit_test_user",
        }

        result = self.service.create_recipe(data, img)
        self.assertIn("data", result)
        recipe = result["data"][0]

        self.assertIn("photopath", recipe)
        self.assertTrue(recipe["photopath"].startswith("http"))

        # cleanup
        rid = recipe["recipeid"]
        delete = self.service.delete_recipe(rid)
        self.assertEqual(delete["message"], "Recipe deleted successfully")


if __name__ == "__main__":
    unittest.main(verbosity=2)
