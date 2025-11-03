import unittest
import json
from app import app  # Flask app entry point
from unittest.mock import patch

class RecipeRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # --- GET ALL RECIPES ---
    @patch("recipe_service.get_all_recipes")
    def test_get_all_recipes(self, mock_get_all_recipes):
        mock_get_all_recipes.return_value = [
            {"recipe_id": 1, "Title": "Brownies"},
            {"recipe_id": 2, "Title": "Cookies"},
        ]
        response = self.app.get("/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Brownies", response.data)

    # --- GET SINGLE RECIPE ---
    @patch("recipe_service.get_recipe_by_id")
    def test_get_single_recipe(self, mock_get_recipe_by_id):
        mock_get_recipe_by_id.return_value = {"recipe_id": 1, "Title": "Brownies"}
        response = self.app.get("/recipes/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Brownies", response.data)

    # --- CREATE RECIPE ---
    @patch("recipe_service.create_recipe")
    def test_create_recipe(self, mock_create_recipe):
        mock_create_recipe.return_value = {"message": "Recipe created successfully"}
        payload = {
            "Title": "Test Brownies",
            "Description": "Rich chocolate brownies",
            "Category": "Dessert",
            "Ingredients": ["flour", "sugar", "cocoa"],
            "Directions": ["mix", "bake", "cool"],
        }
        response = self.app.post(
            "/recipes",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recipe created successfully", response.data)

    # --- UPDATE RECIPE ---
    @patch("recipe_service.update_recipe")
    def test_update_recipe(self, mock_update_recipe):
        mock_update_recipe.return_value = {"message": "Recipe updated successfully"}
        payload = {"Title": "Updated Brownie"}
        response = self.app.put(
            "/recipes/1",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recipe updated successfully", response.data)

    # --- DELETE RECIPE ---
    @patch("recipe_service.delete_recipe")
    def test_delete_recipe(self, mock_delete_recipe):
        mock_delete_recipe.return_value = {"message": "Recipe deleted successfully"}
        response = self.app.delete("/recipes/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recipe deleted successfully", response.data)


if __name__ == "__main__":
    unittest.main()
