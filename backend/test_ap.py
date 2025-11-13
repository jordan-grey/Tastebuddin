import unittest
from recipe_service import RecipeService
from supabase import create_client, Client
import os

class RecipeServiceDatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        cls.supabase: Client = create_client(url, key)

        # Inject Supabase into RecipeService
        cls.service = RecipeService(cls.supabase)

    def test_1_create_recipe(self):
        data = {
            "title": "UnitTest Brownie",
            "description": "A chocolate brownie created by tests.",
            "ingredients": ["flour", "sugar", "cocoa"],
            "directions": ["mix", "bake"],
            "category": "dessert",
            "dietaryrestrictions": ["vegetarian"],
            "minutestocomplete": 30,
            "authorid": "fce74316-e465-412b-8e57-8ff7cbd72d3d",
            "authorname": "test_kadee"
        }
        result = self.service.create_recipe(data)
        #print("Create Response:", result)
        self.assertIn("data", result)

    def test_2_get_all_recipes(self):
        result = self.service.get_all_recipes()
        #print("All Recipes:", result)
        self.assertIn("data", result)

    def test_3_get_single_recipe(self):
        result, status = self.service.get_recipe(1)
        self.assertEqual(status, 200)
        self.assertIn("data", result)

    def test_4_update_recipe(self):
        update_data = {"description": "Updated via unit test!"}
        result = self.service.update_recipe(1, update_data)
        print("Update Response:", result)
        self.assertIn("data", result)

    def test_5_delete_recipe(self):
        """Test deleting an existing recipe."""
        # Step 1: Create a temporary recipe to delete
        recipe_data = {
            "title": "Delete Me Brownie",
            "description": "Temporary record to be deleted.",
            "ingredients": ["flour", "sugar"],
            "directions": ["mix", "bake"],
            "dietaryrestrictions": ["vegetarian"],
            "category": "dessert",
            "authorid": "97c33e9b-e74d-425b-8700-b7aa20ff9da7",
            "authorname": "sarah_test",
            "minutestocomplete": 10,
            "datecreated": "2025-11-07T18:00:00.000000+00:00",
        }

        # Create the recipe first
        create_resp = self.service.create_recipe(recipe_data)
        self.assertIn("data", create_resp)
        new_id = create_resp["data"][0]["recipeid"]

        # Step 2: Delete the recipe
        delete_resp = self.service.delete_recipe(new_id)
        print("Delete Response:", delete_resp)
        self.assertIn("message", delete_resp)
        self.assertEqual(delete_resp["message"], "Recipe deleted successfully")

        # Step 3: Confirm it’s gone
        confirm_resp, status = self.service.get_recipe(new_id)
        result = confirm_resp
        self.assertEqual(status, 404)
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main(verbosity=2)

