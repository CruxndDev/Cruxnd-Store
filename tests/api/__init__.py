import unittest
from app import create_app, database

class TestAppUtils(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.test_client = self.app.test_client()
        self.app_context.push()
        database.create_all()
    
    def tearDown(self) -> None:
        database.drop_all()
        self.app_context.pop()
    
    def test_app_is_not_none(self):
        self.assertIsNotNone(self.app)
    
    def test_wrong_endpoint(self):
        response = self.test_client.get('/wrong/url')
        self.assertEqual(response.status_code, 404)