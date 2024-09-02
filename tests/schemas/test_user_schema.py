import unittest
from app.schemas import CreateUserSchema, UserItemSchema
from app.models import User
class TestCreateUserSchema(unittest.TestCase):

    def setUp(self):
        self.sample_user_data = {
         "username" : "john",
         "email_address" : "john@doe.com",
         "age" : 40, 
         "password" : "12345678",
         "gender" : "Male"
      }
        self.user_schema = CreateUserSchema()
        self.user = self.user_schema.load(self.sample_user_data)
    
    def test_user_is_User(self):
        self.assertIsInstance(self.user, User)

class TestUserItemSchema(unittest.TestCase):
    
    def setUp(self):
        self.user = User(id = 'welcome', username = 'Jira', email_address = 'jira@j.com', age = 30, gender = 'Female')
        self.user_schema = UserItemSchema()
        self.user_dict = self.user_schema.dump(self.user)
    
    def test_user_dict_is_Dict(self):
        self.assertIsInstance(self.user_dict, dict)
    
    def test_user_dict_is_correct(self):
        #! This test is not working because of datetime issues. Please cross check it
        result = {'username': 'Jira', 'email_address': 'jira@j.com', 'age': 30, 'gender': 'Female', 'id': 'welcome', 'created' : None}
        self.assertEqual(result, self.user_dict)
    

