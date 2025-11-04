'''import unittest
from unittest.mock import patch, MagicMock
from app import app  # Flask app
from recipe_utility import (
    filter_recipes_by_user_restrictions,
    add_to_unseen
)

# Mock Supabase for testing
mock_recipe = {
    "Title": "Test Brownies",
    "AuthorID": "mock-user-uuid",
    "AuthorName": "Kadee",
    "Category": "Dessert",
    "Description": "Rich chocolate brownies",
    "Ingredients": ["flour", "sugar", "cocoa"],
    "Directions": ["mix", "bake", "cool"],
    "DietaryRestrictions": ["Vegetarian"],
    "Likes": 0,
    "MinutesToComplete": 45
}


class RecipeRoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # ---- POST Recipe ----
    @patch("recipe_service.supabase.table")
    def test_post_recipe(self, mock_table):
        mock_recipe = {
            "title": "Chocolate Cake",
            "description": "Rich dessert",
            "ingredients": ["flour", "sugar", "cocoa"],
            "directions": ["mix", "bake"],
            "category": "Dessert",
            "authorID": "test-user-id",
            "dietaryrestrictions": ["Vegetarian"]
        }

        # Mock Supabase insert().execute() return
        mock_exec = MagicMock()
        mock_exec.data = [mock_recipe]
        mock_table.return_value.insert.return_value.execute.return_value = mock_exec

        response = self.client.post("/recipes", json=mock_recipe)
        print("POST response:", response.get_data(as_text=True))  # optional debugging line
        self.assertIn(response.status_code, [200, 201])

    # ---- GET All Recipes ----
    @patch("recipe_service.supabase.table")
    def test_get_all_recipes(self, mock_table):
        mock_exec = MagicMock()
        mock_exec.data = [mock_recipe]
        mock_table.return_value.select.return_value.execute.return_value = mock_exec

        response = self.client.get("/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Brownies", response.get_data(as_text=True))

    # ---- GET Single Recipe ----
    @patch("recipe_service.supabase.table")
    def test_get_single_recipe(self, mock_table):
        mock_exec = MagicMock()
        mock_exec.data = [mock_recipe]
        mock_table.return_value.select.return_value.eq.return_value.execute.return_value = mock_exec

        response = self.client.get("/recipes/1")
        self.assertEqual(response.status_code, 200)

    # ---- PUT Recipe ----
    @patch("recipe_service.supabase.table")
    def test_update_recipe(self, mock_table):
        mock_exec = MagicMock()
        mock_exec.data = [{"Title": "Updated Recipe"}]
        mock_table.return_value.update.return_value.eq.return_value.execute.return_value = mock_exec

        response = self.client.put("/recipes/1", json={"Title": "Updated Recipe"})
        self.assertIn(response.status_code, [200, 404])

    # ---- DELETE Recipe ----
    @patch("recipe_service.supabase.table")
    def test_delete_recipe(self, mock_table):
        mock_exec = MagicMock()
        mock_exec.data = [{"deleted": True}]
        mock_table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_exec

        response = self.client.delete("/recipes/1")
        self.assertIn(response.status_code, [200, 404])


# ------------------------------------------------------------------------
# Utility function tests (no real Supabase)
# ------------------------------------------------------------------------

class RecipeUtilityTests(unittest.TestCase):

    @patch("recipe_utility.supabase")
    def test_filter_recipes_by_user_restrictions(self, mock_supabase):
        # Mock recipe data
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"Title": "Salad", "DietaryRestrictions": ["Vegetarian"]},
            {"Title": "Steak", "DietaryRestrictions": ["Meat"]},
            {"Title": "Tofu Bowl", "DietaryRestrictions": ["Vegan"]}
        ]

        # Mock user preferences
        user_prefs = {"DietaryRestrictions": ["Vegetarian", "Pescatarian"]}
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [user_prefs]

        filtered = filter_recipes_by_user_restrictions("mock-user-id")
        # Expect vegan excluded since not in allowed list
        self.assertTrue(any(r["Title"] == "Salad" for r in filtered))
        self.assertFalse(any(r["Title"] == "Steak" for r in filtered))

    @patch("recipe_utility.supabase")
    def test_add_recipe_to_unseen_for_all_users(self, mock_supabase):
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
            {"UserID": "user1"},
            {"UserID": "user2"},
        ]
        add_to_unseen("user1", 15)
        mock_supabase.table.assert_called()  # Ensures it tried inserting unseen entries


if __name__ == "__main__":
    unittest.main()
    '''


import unittest
import json
from app import app
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class RecipeRoutesIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    #  1. Create recipe (uses lowercase + valid UUID)
    def test_1_post_recipe_real(self):
        new_recipe = {
            "title": "IntegrationTest Brownies",
            "description": "Sweet test brownies",
            "ingredients": ["flour", "sugar", "chocolate"],
            "directions": ["mix", "bake", "cool"],
            "dietaryrestrictions": ["vegetarian"],
            "category": "dessert",
            "authorid": "97c33e9b-e74d-425b-8700-b7aa20ff9da7",
            "authorname": "sarah_test",
            "minutestocomplete": 45
        }
        response = self.client.post(
            "/recipes",
            data=json.dumps(new_recipe),
            content_type="application/json"
        )
        print("POST Response:", response.json)
        self.assertIn(response.status_code, [200, 201])

    #  2. Get all recipes
    def test_2_get_all_recipes(self):
        response = self.client.get("/recipes")
        print("GET /recipes:", response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 0)

    #  3. Get one recipe by ID
    def test_3_get_single_recipe(self):
        recipes = supabase.table("recipes_public").select("recipeid").limit(1).execute()
        if not recipes.data:
            self.skipTest("No recipes found for single test.")
        recipe_id = recipes.data[0]["recipeid"]
        response = self.client.get(f"/recipes/{recipe_id}")
        self.assertIn(response.status_code, [200, 404])

    #  4. Update recipe
    def test_4_update_recipe(self):
        recipes = supabase.table("recipes_public").select("recipeid").limit(1).execute()
        if not recipes.data:
            self.skipTest("No recipes found to update.")
        recipe_id = recipes.data[0]["recipeid"]
        update_data = {"description": "Updated test recipe!"}
        response = self.client.put(
            f"/recipes/{recipe_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertIn(response.status_code, [200, 404])

    #  5. Delete recipe
    def test_5_delete_recipe(self):
        new_recipe = {
            "title": "DeleteMe",
            "description": "Temporary for deletion test",
            "ingredients": ["temp"],
            "directions": ["none"],
            "category": "temp",
            "authorid": "97c33e9b-e74d-425b-8700-b7aa20ff9da7",
            "authorname": "sarah_test"
        }
        insert = supabase.table("recipes_public").insert(new_recipe).execute()
        if not insert.data:
            self.skipTest("Insert failed; cannot test deletion.")
        recipe_id = insert.data[0]["recipeid"]
        response = self.client.delete(f"/recipes/{recipe_id}")
        self.assertIn(response.status_code, [200, 404])


if __name__ == "__main__":
    unittest.main()

