import unittest
from app import create_app, database


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()

    def tearDown(self):
        self.app_context.pop()
        database.drop_all()

    def test_users_get(self):
        response = self.client.get("/v1/users")
        self.assertEqual(response.status_code, 200)

    def test_users_post(self):
        payload = {
            "username": "Mary",
            "email_address": "mary@mar.com",
            "age": 20,
            "password": "12345678",
            "gender": "female",
        }
        response = self.client.post("/v1/users", json=payload)
        self.assertEqual(response.status_code, 201)
