import unittest
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # * Adding the tests to the app path
from app.models import User, Cart, Product

u1 = User(username = "myuser", password = 'mypassword', email_address = 'user@email.com')
p1 = Product(name = "tea", price = 400.50)
c1 = Cart(name = "my cart")

class TestProduct(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        c1.creator = u1
        p1.buy(u1)

    @classmethod
    def tearDownClass(cls) -> None:
        c1.creator = None
        p1.buyer = None

    def test_product_is_not_none(self):
        self.assertIsNotNone(p1)

    def test_product_is_bought(self):
        self.assertTrue(p1.is_bought)
