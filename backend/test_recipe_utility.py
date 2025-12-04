"""
File Name: recipe_utility_test.py
Purpose: Unit tests for the RecipeUtility class, verifying allergen filtering,
         unseen recipe filtering, and feed generation logic used in the
         Tastebuddin recipe-recommendation system.

System Context:
    This file is part of the Tastebuddin backend test suite. It ensures the
    correctness of RecipeUtility, which performs allergen filtering,
    unseen-recipe filtering, and feed computation for personalized user feeds.

Created On: 2025-12-04
Authors: Kadee Wheeler

"""

import unittest
from recipe_utility import RecipeUtility


class RecipeUtilityTest(unittest.TestCase):
    """Tests for the RecipeUtility class methods."""

    @classmethod
    def setUpClass(cls):
        cls.utility = RecipeUtility()
        # Mock recipe data
        cls.recipes = [
            {
                "recipeid": 1,
                "title": "Peanut Butter Cookies",
                "ingredients": ["flour", "peanuts", "sugar"],
                "dietaryrestrictions": [],
            },
            {
                "recipeid": 2,
                "title": "Grilled Salmon",
                "ingredients": ["fish", "salt", "lemon"],
                "dietaryrestrictions": ["pescatarian"],
            },
            {
                "recipeid": 3,
                "title": "Chocolate Cake",
                "ingredients": ["flour", "sugar", "cocoa"],
                "dietaryrestrictions": ["vegetarian"],
            },
        ]

        # Mock user profiles
        cls.user_safe = {
            "allergens": [],
            "unseen_recipes": [1, 2, 3],
        }

        cls.user_with_allergies = {
            "allergens": ["peanuts", "fish"],
            "unseen_recipes": [1, 2, 3],
        }

        cls.user_with_unseen = {
            "allergens": [],
            "unseen_recipes": [3],
        }

    def test_filter_recipes_by_allergens(self):
        """Test allergen filtering removes recipes containing user allergens."""
        safe_recipes = self.utility.filter_recipes_by_allergens(
            self.recipes, self.user_with_allergies["allergens"]
        )
        titles = [r["title"] for r in safe_recipes]
        self.assertNotIn("Peanut Butter Cookies", titles)
        self.assertNotIn("Grilled Salmon", titles)
        self.assertIn("Chocolate Cake", titles)

    def test_filter_unseen_recipes(self):
        """Test unseen filtering only includes recipes user hasn't seen."""
        unseen_only = self.utility.filter_unseen_recipes(
            self.recipes, self.user_with_unseen["unseen_recipes"]
        )
        self.assertEqual(len(unseen_only), 1)
        self.assertEqual(unseen_only[0]["title"], "Chocolate Cake")

    def test_generate_user_feed(self):
        """Test combined allergen + unseen filtering produces correct feed."""
        feed = self.utility.generate_user_feed(self.recipes, self.user_with_allergies)
        titles = [r["title"] for r in feed]
        self.assertIn("Chocolate Cake", titles)
        self.assertNotIn("Peanut Butter Cookies", titles)
        self.assertNotIn("Grilled Salmon", titles)

    def test_generate_user_feed_with_no_allergens(self):
        """Test feed generation works for users with no allergens."""
        feed = self.utility.generate_user_feed(self.recipes, self.user_safe)
        self.assertEqual(len(feed), 3)

if __name__ == "__main__":
    unittest.main()
