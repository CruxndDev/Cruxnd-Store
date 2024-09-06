import unittest
from sqlalchemy.orm.collections import InstrumentedList

import os, sys

from app.models import User, Cart, Product

u1 = User(username = "myuser", password = 'mypassword', email_address = 'user@email.com')
p1 = Product(name = "tea", price = 400.50)
c1 = Cart(name = "my cart")

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        c1.creator = u1
        p1.buy(u1)

    @classmethod
    def tearDownClass(cls) -> None:
        c1.creator = None
        p1.buyer = None

    def test_user_is_not_none(self):
        self.assertIsNotNone(u1)

    def test_user_password_inaccessible(self):
        with self.assertRaises(AttributeError):
            u1.password

    def test_user_has_cart(self):
        self.assertIsInstance(u1.carts, InstrumentedList)  # * From sqlalchemy

    def test_user_buys_product(self):
        self.assertIsInstance(u1.products_bought, InstrumentedList)

    def test_users_different_password(self):
        u2 = User(
            username="John",
            email_address="john@doe.com",
            age=30,
            gender="Male",
            password="12345678",
        )  # * #type: ignore make sure two users with the same details dont have the same passwrord

        self.assertNotEqual(u1.password_hash, u2.password_hash)
