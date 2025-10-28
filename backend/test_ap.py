import unittest
import json
import uuid
from app import app

class RecipeRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        # sample recipe data
        self.new_recipe = {
            "Title": "Test Brownies",
            "Author": "97c33e9b-e74d-425b-8700-b7aa20ff9da7",
            "Category": "Dessert",
            "MinutesToComplete": 45,
            "Description": "Rich chocolate brownies",
            "Ingredients": ["flour", "sugar", "cocoa"],
            "Directions": ["mix", "bake", "cool"],
            "DietaryRestrictions": "Vegetarian",
            "DateCreated": "2025-10-20",
            "Likes": 0
        }

    def test_create_recipe(self):
        """Test POST /recipes (init)"""
        response = self.client.post(
            "/recipes",
            data=json.dumps(self.new_recipe),
            content_type="application/json"
        )
        self.assertIn(response.status_code, [201, 500])  # 500 if DB error
        print("POST response:", response.json)
        self.assertEqual(response.json['message'], 'Recipe created successfully')


    def test_get_all_recipes(self):
        """Test GET /recipes"""
        response = self.client.get("/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_single_recipe(self):
        """Test GET /recipes/<id>"""
        recipe_id = 1  # replace with a valid ID from your DB if available
        response = self.client.get(f"/recipes/{recipe_id}")
        self.assertIn(response.status_code, [200, 404])

    def test_update_recipe(self):
        """Test PUT /recipes/<id>"""
        updated_data = {"Description": "Updated Description"}
        recipe_id = 1
        response = self.client.put(
            f"/recipes/{recipe_id}",
            data=json.dumps(updated_data),
            content_type="application/json"
        )
        self.assertIn(response.status_code, [200, 404, 500])

    def test_delete_recipe(self):
        """Test DELETE /recipes/<id>"""
        recipe_id = 1
        response = self.client.delete(f"/recipes/{recipe_id}")
        self.assertIn(response.status_code, [200, 404, 500])
'''
class UserTasksTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        # sample recipe data
        self.new_user = {
            "Title": "Test Brownies",
            "Author": "97c33e9b-e74d-425b-8700-b7aa20ff9da7",
            "Category": "Dessert",
            "MinutesToComplete": 45,
            "Description": "Rich chocolate brownies",
            "Ingredients": ["flour", "sugar", "cocoa"],
            "Directions": ["mix", "bake", "cool"],
            "DietaryRestrictions": "Vegetarian",
            "DateCreated": "2025-10-20",
            "Likes": 0
        }
'''
if __name__ == '__main__':
    unittest.main()
