import unittest
import uuid
import os
from supabase import create_client
from user_service import UserService
from dotenv import load_dotenv

load_dotenv()

class UserServiceDatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to Supabase
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        cls.supabase = create_client(url, key)

        cls.service = UserService(cls.supabase)

        cls.test_password = "Password123!"

        # ---------------------------------------------------------
        # Create MAIN TEST USER
        # ---------------------------------------------------------
        cls.test_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"

        auth_res = cls.supabase.auth.sign_up({
            "email": cls.test_email,
            "password": cls.test_password
        })

        cls.user_id = auth_res.user.id

        cls.service.create_user(cls.user_id, username="test_user")

        # ---------------------------------------------------------
        # Create AUTHOR USER
        # ---------------------------------------------------------
        cls.author_email = f"author_{uuid.uuid4().hex[:6]}@example.com"

        auth_author = cls.supabase.auth.sign_up({
            "email": cls.author_email,
            "password": cls.test_password
        })

        cls.author_id = auth_author.user.id

        cls.service.create_user(cls.author_id, username="author_test")

    # ---------------------------------------------------------
    def test_1_create_user(self):
        user, status = self.service.get_user(self.user_id)
        self.assertEqual(status, 200)
        self.assertIn("data", user)

    # ---------------------------------------------------------
    def test_2_get_user(self):
        user, status = self.service.get_user(self.user_id)
        self.assertEqual(status, 200)
        self.assertEqual(user["data"][0]["username"], "test_user")

    # ---------------------------------------------------------
    def test_3_update_allergens(self):
        allergens = ["peanuts", "gluten"]

        result, status = self.service.update_allergens(self.user_id, allergens)
        self.assertEqual(status, 200)

        # Fetch updated user
        updated, _ = self.service.get_user(self.user_id)
        self.assertEqual(updated["data"][0]["allergens"], allergens)

    # ---------------------------------------------------------
    def test_4_like_recipe(self):
        recipe_id = 1001

        result, status = self.service.like_recipe(self.user_id, recipe_id, self.author_id)
        self.assertEqual(status, 200)

        user, _ = self.service.get_user(self.user_id)
        self.assertIn(recipe_id, user["data"][0]["liked_recipes"])

    # ---------------------------------------------------------
    def test_5_unlike_recipe(self):
        recipe_id = 1001

        result, status = self.service.unlike_recipe(self.user_id, recipe_id, self.author_id)
        self.assertEqual(status, 200)

        user, _ = self.service.get_user(self.user_id)
        self.assertNotIn(recipe_id, user["data"][0]["liked_recipes"])

    # ---------------------------------------------------------
    def test_6_add_unseen(self):
        recipe_id = 2002

        result, status = self.service.add_unseen(self.user_id, recipe_id)
        self.assertEqual(status, 200)

        user, _ = self.service.get_user(self.user_id)
        self.assertIn(recipe_id, user["data"][0]["unseen_recipes"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
