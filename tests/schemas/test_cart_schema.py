import unittest
from app.schemas import CreateCartSchema, CartItemSchema
from app.models import Cart
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")


class TestCartItemSchema(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(products=["Iphone 12", "Samsung S20 Ultra"])
        self.cart_schema = CartItemSchema()
        self.cart_dict = self.cart_schema.dump(self.cart)

    def test_cart_dict_is_Dict(self):
        self.assertIsInstance(self.cart_dict, dict)


class TestCreateCartSchema(unittest.TestCase):

    def setUp(self):
        self.sample_cart_data = {"products": ["iphone 15", "Samsung 60"]}
        self.cart_schema = CreateCartSchema()
        self.cart = self.cart_schema.load(self.sample_cart_data)

    def test_cart_is_Cart(self):
        self.assertIsInstance(self.cart, Cart)

    def test_cart_product_data(self):
        self.assertEqual(self.cart.products, ["iphone 15", "Samsung 60"])
