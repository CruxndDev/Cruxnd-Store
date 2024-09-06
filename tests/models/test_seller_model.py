import unittest
from sqlalchemy.orm.collections import InstrumentedList

import os, sys


from app.models import Seller, User, Cart, Product

u1 = User(username = "myuser", password = 'mypassword', email_address = 'user@email.com')
p1 = Product(name = "tea", price = 400.50)
c1 = Cart(name = "my cart")
s1 = Seller.from_user(u1)
products = ["Phone","Tablet","Laptop","PC","Fish"]

class TestSeller(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        s1.products = ""

    def test_seller_is_not_none(self):
        self.assertIsNotNone(s1)

    def test_seller_from_user(self):
        self.assertIsInstance(s1, Seller)
