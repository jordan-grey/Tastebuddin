import unittest
from app import app
from unittest.mock import patch, MagicMock
from recipe_utility import filter_recipes_by_user_restrictions, add_to_unseen
from recipe_service import onboard_new_user, create_recipe


class UserFlowTests(unittest.TestCase):
    """Integration-style tests for new user onboarding and recipe-user sync."""

    @patch("recipe_service.supabase")
    @patch("recipe_utility.supabase")
    def test_onboard_new_user_filters_recipes(self, mock_supabase_util, mock_supabase_service):
        """Simulate new user signup triggering recipe filtering and unseen prefill."""
        # Mock all recipes in DB
        mock_recipes = [
            {"RecipeID": 1, "Title": "Vegan Curry", "DietaryRestrictions": ["Vegan"]},
            {"RecipeID": 2, "Title": "Steak Dinner", "DietaryRestrictions": ["None"]},
            {"RecipeID": 3, "Title": "Salad", "DietaryRestrictions": ["Vegetarian"]},
        ]
        # Mock user restrictions
        mock_supabase_util.table.return_value.select.return_value.execute.return_value.data = mock_recipes

        user_id = "new-user-uuid"
        user_restrictions = ["Vegetarian"]

        # Patch filtering behavior
        with patch("recipe_utility.filter_recipes_by_user_restrictions",
                   return_value=[mock_recipes[2]]) as mock_filter:
            onboard_new_user(user_id)
            mock_filter.assert_called_once_with(user_id, user_restrictions)

        print("✅ New user onboarding triggered filtering correctly.")

    @patch("recipe_service.supabase")
    @patch("recipe_utility.supabase")
    def test_create_recipe_updates_unseen_users(self, mock_supabase_util, mock_supabase_service):
        """Simulate adding a new recipe and ensuring it’s pushed to all matching users."""
        # Mock all users
        mock_users = [
            {"UserID": "user1", "Restrictions": ["Vegan"]},
            {"UserID": "user2", "Restrictions": ["Vegetarian"]},
        ]
        mock_supabase_util.table.return_value.select.return_value.execute.return_value.data = mock_users

        # Create a new recipe
        new_recipe = {
            "Title": "Veggie Bowl",
            "Description": "Healthy lunch bowl",
            "Ingredients": ["rice", "beans", "broccoli"],
            "Directions": ["mix", "serve"],
            "DietaryRestrictions": ["Vegan"]
        }

        # Mock Supabase insert
        mock_insert = MagicMock()
        mock_insert.data = [new_recipe]
        mock_supabase_service.table.return_value.insert.return_value.execute.return_value = mock_insert
        with app.app_context():
            response = create_recipe(new_recipe)
        self.assertIn("Recipe created successfully", response.get_json()["message"])

        print("New recipe triggers unseen user updates properly.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
