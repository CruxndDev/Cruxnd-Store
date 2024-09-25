import unittest
from app import create_app, database

class TestSeller(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()

    def tearDown(self):
        self.app_context.pop()
        database.drop_all()
    
    def test_sellers_get(self):
        response = self.client.get('/v1/sellers')
        self.assertEqual(response.status_code, 200)
    
    def test_get_seller(self):
        response = self.client.get('/v1/sellers/1')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_seller(self):
        response = self.client.delete('/v1/sellers/1')
        self.assertEqual(response.status_code, 404)
        