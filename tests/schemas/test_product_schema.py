import unittest
from app.schemas import CreateProductSchema, ProductItemSchema
from app.models import Product, User
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")


class TestCreateProductSchema(unittest.TestCase):

    def setUp(self):
        self.sample_product_data = {"name": "Iphone 20", "price": 400.50}
        self.product_schema = CreateProductSchema()
        self.product = self.product_schema.load(self.sample_product_data)

    def test_product_is_Product(self):
        self.assertIsInstance(self.product, Product)


class TestProductItemSchema(unittest.TestCase):

    def setUp(self):
        self.product = Product(id="Hey", is_bought=False, name="Iphone 12", price=3000)
        self.product_schema = ProductItemSchema()
        self.product_dict = self.product_schema.dump(self.product)

    def test_product_dict_is_Dict(self):
        self.assertIsInstance(self.product_dict, dict)

    def test_product_dict_is_correct(self):
        result = {
            "name": "Iphone 12",
            "price": 3000.0,
            "id": "Hey",
            "created": None,
            "updated": None,
            "is_bought": False,
            "url": f"{SERVER_URL}/products/Hey",
            "buyer" : None,
        }
        self.assertEqual(result, self.product_dict)

    def test_product_is_bought(self):
        self.product.buy(
            User()
        )  # * All required columns are checked on database commit
        self.product_dict = self.product_schema.dump(self.product)
        self.assertTrue(self.product_dict["is_bought"])
