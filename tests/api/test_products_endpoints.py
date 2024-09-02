import unittest
from app import create_app, database

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing') 
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()
    
    def tearDown(self):
        self.app_context.pop()
        database.drop_all()
    
    def test_products_url(self):
        response = self.client.get('/v1/products')
        self.assertEqual(response.status_code, 200)