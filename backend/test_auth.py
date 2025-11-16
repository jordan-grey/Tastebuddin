
import unittest
from user import user
import json
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
        self.test_user_data = {"username": 'testuser1', 
             "email": "testuser1@gmail.com", 
             "password": "GeeksforGeeks2",
             "allergens":["peanuts", "treenuts"]}
        self.uuid = "fce74316-e465-412b-8e57-8ff7cbd72d3d"

    def test_a_insert_public_users(self):
        test_user = user(self.test_user_data, self.uuid)
        result = test_user.create_profile()
        self.assertEqual(result["message"],  "Profile created successfully")

    def test_b_pull_data_users(self):   
        data = user.get_user_with_id(self.uuid)
        self.assertEqual(data.data[0]['username'],  'testuser1')
"""
    def test_c_delete_user(self):
        data = user.delete_profile(self.uuid)
        print(data)
        self.assertEqual(data.data[0]['username'],  'testuser1')
"""
  

if __name__ == '__main__':
    unittest.main()