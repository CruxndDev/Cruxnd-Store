import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #* Adding the tests to path so that it can see the app
from app import create_app, database
from app.fake import create_carts, create_products, create_sellers, create_users

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing') 
        self.client = self.app.test_client()
        self.app.app_context().push()
        database.create_all()
        create_users(20) #* create 20 users
        create_sellers(10) #* create 10 sellers
        create_products(30) #* create 30 products
        create_carts(5) #* create 5 carts
    
    def tearDown(self):
        database.drop_all()
    
    def test_products_url(self):
        response = self.client.get('/v1/products')
        self.assertEqual(response.status_code, 200)