import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #* Adding the tests to path so that it can see the app

from sqlalchemy.orm.collections import InstrumentedList

from app.models import User, Product, Cart, Seller, generate_user_id

u1 = User(username = "John", email_address = "john@doe.com", age = 30, gender = "Male", password = "12345678") 
p1= Product(name = "Samsung Wink 20", price = 400.50) 
products = ["Phone","Tablet","Laptop","PC","Fish"]
s1 = Seller.from_user(u1)
c1 = Cart(name = "myCart", products_list = products, creator = u1) 

class TestUtilities(unittest.TestCase):

    def test_uuid(self):
        self.assertEqual(len(generate_user_id()), 36)
    
class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        c1.creator = u1
        p1.buy(u1)
    
    @classmethod
    def tearDownClass(cls) -> None:
        c1.creator = None 
        p1.buyer  = None

    def test_user_is_not_none(self):
        self.assertIsNotNone(u1)
    
    def test_user_password_inaccessible(self):
        with self.assertRaises(AttributeError):
            u1.password
    
    def test_user_has_cart(self):
        self.assertEqual(type(u1.carts), InstrumentedList) #* From sqlalchemy
    
    def test_user_buys_product(self):
        self.assertEqual(type(u1.products_bought), InstrumentedList)
        
    def test_users_different_password(self):
        u2 = User(username = "John", email_address = "john@doe.com", age = 30, gender = "Male", password = "12345678") #* #type: ignore make sure two users with the same details dont have the same passwrord

        self.assertNotEqual(u1.password_hash, u2.password_hash)
    

class TestProduct(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        c1.creator = u1
        p1.buy(u1)
    
    @classmethod
    def tearDownClass(cls) -> None:
        c1.creator = None 
        p1.buyer  = None

    def test_product_is_not_none(self):
        self.assertIsNotNone(p1)
    
    def test_product_is_bought(self):
        self.assertTrue(p1.is_bought)
    
    def test_product_has_buyer(self):
        self.assertEqual(type(p1.buyer), type(u1))

class TestSeller(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        [s1.add_product(product) for product in products]
    
    @classmethod
    def tearDownClass(cls) -> None:
        s1.products = ''
    
    def test_seller_is_not_none(self):
        self.assertIsNotNone(s1)
    
    def test_set_seller_products(self):
        self.assertEqual(s1.products,'Phone,Tablet,Laptop,PC,Fish,Hey')
    
    def test_seller_add_product(self):
        s1.add_product("Hey")
        self.assertEqual(s1.products.split(',')[-1], "Hey")
    
    def test_seller_from_user(self):
        self.assertEqual(type(s1), Seller)

class TestCart(unittest.TestCase):

    def test_cart_is_not_none(self):
        self.assertIsNotNone(c1)
    
    def test_set_cart_products(self):
        self.assertEqual(c1.products , 'Phone,Tablet,Laptop,PC,Fish', )
    
    def test_cart_has_creator(self):
        self.assertEqual(type(c1.creator), User)
        