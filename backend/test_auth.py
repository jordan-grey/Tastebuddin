
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

    def test_c_delete_user(self):
        data = user.delete_profile(self.uuid)
        print(data)
        self.assertEqual(data.data[0]['username'],  'testuser1')
"""
    def test_create_profile(self):
        test_user = user(self.test_user_data)
        test_user.create_auth()
        test_user.create_profile()
        # check if user was created
        data = user.get_user_with_id(test_user)
        decoded = json.load(data)
        self.assertEqual(decoded["username"], self.test_user_data.username)
"""   
'''
    def test_register(self, test_user):
        """Test GET /recipes"""
        response = app.auth.sign_up(    
            {        
                "email": self.,
                "password": self.password,
            }
        )
        self.auth.id = test_user.user.id
        self.assertEqual(test_user.session.aud, "authenticated")

    def test_deletetester(self):
        response = delete_account(self.auth.id)
        self.assertEqual(response.status_code, 200)
'''

if __name__ == '__main__':
    unittest.main()