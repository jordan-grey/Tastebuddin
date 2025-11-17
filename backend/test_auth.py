import unittest
from backend.user import User
import json
import os
from supabase import create_client, Client
"""
peanuts 
fish
shellfish
gluten
dairy
treenuts
"""

class UserTasksTestCase(unittest.TestCase):
    def setUp(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")

        self.supabase: Client = create_client(url, key)
        self.test_user_data = {"username": 'testuser1', 
             "email": "testuser1@gmail.com", 
             "password": "GeeksforGeeks2",
             "allergens":["peanuts", "treenuts"]}
        self.uuid = "fce74316-e465-412b-8e57-8ff7cbd72d3d"

    def test_a_insert_public_users(self):
        test_user = User(self.supabase, self.uuid)
        result = test_user.create_profile(self.test_user_data)
        self.assertEqual(result["message"],  "Profile created successfully")

    def test_b_pull_data_users(self):   
        data = User.get_user_with_id(self.supabase, self.uuid)
        self.assertEqual(data.data[0]['username'],  'testuser1')

    def test_c_delete_user(self):
        data = User.delete_profile(self.supabase, self.uuid)
        print(data)
        self.assertEqual(data.data[0]['username'],  'testuser1')

  

if __name__ == '__main__':
    unittest.main()