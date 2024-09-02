import unittest
import os, sys

from app.models import User, Cart, Product

u1 = User(username = "myuser", password = 'mypassword', email_address = 'user@email.com')
p1 = Product(name = "tea", price = 400.50)
c1 = Cart(name = "my cart")


class TestCart(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        c1.creator = u1

    def test_cart_is_not_none(self):
        self.assertIsNotNone(c1)

    def test_cart_has_creator(self):
        self.assertIsInstance(c1.creator, User)
