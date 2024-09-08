import unittest
from app import create_app, database


class TestProductEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()

    def tearDown(self):
        self.app_context.pop()
        database.drop_all()

    def test_products_get(self):
        response = self.client.get("/v1/products")
        self.assertEqual(response.status_code, 200)

    def test_products_post(self):
        payload = {"name": "Silver", "price": 29000.00}
        response = self.client.post("/v1/products?sellerid=1", json=payload)
        self.assertEqual(response.status_code, 404)
        
        response = self.client.post('/v1/products', json=payload)
        self.assertEqual(response.status_code,400)

    def test_product_item_get(self):
        response = self.client.get("/v1/products/1")
        self.assertEqual(response.status_code, 404)

    def test_product_item_put(self):
        payload = {"name": "Diamond", "price": 23500.00}
        response = self.client.put("/v1/products/5?sellerid=1", json=payload)
        self.assertEqual(response.status_code, 404)
    
    def test_product_item_delete(self):
        response = self.client.delete("/v1/products/5")
        self.assertEqual(response.status_code, 400)
    
    def test_product_item_buy(self):
        response = self.client.post('/v1/products/5')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/v1/products/5?buyerid=2')
        self.assertEqual(response.status_code, 404)