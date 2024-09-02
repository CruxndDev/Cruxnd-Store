import unittest
from app.schemas import SellerItemSchema
from app.models import Seller
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")


class TestSellerItemSchema(unittest.TestCase):

    def setUp(self):
        self.seller = Seller(products=["Iphone12", "SamsungS20Ultra"])
        self.seller_schema = SellerItemSchema()
        self.seller_dict = self.seller_schema.dump(self.seller)

    def test_seller_dict_is_Dict(self):
        self.assertIsInstance(self.seller_dict, dict)

    def test_seller_dict_is_correct(self):
        result = {
            "username": None,
            "email_address": None,
            "age": None,
            "gender": None,
            "id": None,
            "created": None,
            "products": ["Iphone12", "SamsungS20Ultra"],
            "products_url": [f'{SERVER_URL}/products/Iphone12', f'{SERVER_URL}/products/SamsungS20Ultra'],
            "products_number" : 2
        }
        self.assertEqual(result, self.seller_dict)
