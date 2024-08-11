import unittest

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #* Adding the tests to path so that it can see the app

from app.schemas import CartItemSchema, CreateUserSchema, CreateProductSchema, CreateCartSchema, ProductItemSchema, SellerItemSchema, UserItemSchema
from app.models import Cart, Seller, User, Product

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
    
class TestCreateProductSchema(unittest.TestCase):

    def setUp(self):
        self.sample_product_data = {
         "name" : "Iphone 20",
         "price" : 400.50
        }
        self.product_schema = CreateProductSchema()
        self.product = self.product_schema.load(self.sample_product_data)
    
    def test_product_is_Product(self):
        self.assertIsInstance(self.product, Product)

class TestCreateCartSchema(unittest.TestCase):

    def setUp(self):
        self.sample_cart_data = {
         "products_list" : ["iphone 15", "Samsung 60"]
      }
        self.cart_schema = CreateCartSchema()
        self.cart = self.cart_schema.load(self.sample_cart_data)
    
    def test_cart_is_Cart(self):
        self.assertIsInstance(self.cart, Cart)
    
    def test_cart_product_data(self):
        self.assertEqual(self.cart.products, 'iphone 15,Samsung 60')
    
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
    
class TestProductItemSchema(unittest.TestCase):

    def setUp(self):
        self.product = Product(id = "Hey", is_bought = False, name = "Iphone 12", price = 3000)
        self.product_schema = ProductItemSchema()
        self.product_dict = self.product_schema.dump(self.product)
    
    def test_product_dict_is_Dict(self):
        print(self.product_dict)
        self.assertIsInstance(self.product_dict, dict)
    
    def test_product_dict_is_correct(self):
        result = {'name': 'Iphone 12', 'price': 3000.0, 'id': 'Hey', 'created': None, 'updated': None, 'is_bought': False}
        self.assertEqual(result, self.product_dict)
        
    
    def test_product_is_bought(self):
        self.product.buy(User())  #* All required columns are checked on database commit
        self.product_dict = self.product_schema.dump(self.product)
        self.assertTrue(self.product_dict['is_bought'])

class TestCartItemSchema(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(products = "Iphone 12,Samsung S20 Ultra")
        self.cart_schema = CartItemSchema()
        self.cart_dict = self.cart_schema.dump(self.cart)
    
    def test_cart_dict_is_Dict(self):
        self.assertIsInstance(self.cart_dict, dict)
    
    def test_cart_dict_is_correct(self):
        result = {'products_list': ['Iphone 12', 'Samsung S20 Ultra']}
        self.assertEqual(result, self.cart_dict)
    
class TestSellerItemSchema(unittest.TestCase):
     
    def setUp(self):
        self.seller = Seller(products = "Iphone 12,Samsung S20 Ultra")
        self.seller_schema = SellerItemSchema()
        self.seller_dict = self.seller_schema.dump(self.seller)
    
    def test_seller_dict_is_Dict(self):
        self.assertIsInstance(self.seller_dict, dict)
    
    def test_seller_dict_is_correct(self):
        result =  {'username': None, 'email_address': None, 'age': None, 'gender': None, 'id': None, 'created': None, 'products_list': ['Iphone 12', 'Samsung S20 Ultra']}
        self.assertEqual(result, self.seller_dict)