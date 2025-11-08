
import unittest
from backend.user import user
import json
"""
peanuts 
fish
shellfish
gluten
dairy
treenuts
"""


test_user_data = {"username": 'testuser', 
             "email": 'testuser@gmail.com', 
             "password": 'Geeks',
             "allergens":["peanuts", "treenuts"]}
class UserTasksTestCase(unittest.TestCase):
    def setUp(self):
        test_user = user(test_user_data)
        test_user.create_profile()
        # check if user was created
        data = user.get_user_with_id(test_user)
        decoded = json.load(data)
        self.assertEqual(decoded["username"], test_user_data.username)
        
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