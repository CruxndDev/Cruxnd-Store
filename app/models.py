"""
* Models file for store api to handle database structure
"""

from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from app import database

def generate_user_id():
    return str(uuid4())

class User(database.Model):
    """
    A User in the cruxnd store
    """
    id: str = database.Column(database.String(36), primary_key = True, default = generate_user_id)
    password_hash: str = database.Column(database.String(128))
    username: str = database.Column(database.String(50), nullable = False)
    email_address: str = database.Column(database.String(100), nullable = False)
    age: int = database.Column(database.Integer(), nullable = False)
    gender: str = database.Column(database.String(10), nullable = False)
    created: datetime = database.Column(database.DateTime(), default = datetime.now)
    seller = database.relationship('Seller', backref = 'user')
    carts = database.relationship('Cart', backref = 'user')
    products_bought = database.relationship('Product', backref = 'user')

    @property
    def password(self):
        raise AttributeError("Password cant be accessed directly")

    @password.setter
    def password(self, value: str):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, user_input: str):
        return check_password_hash(self.password_hash, user_input)


class Product(database.Model):
    id: str = database.Column(database.String(36), primary_key = True, default = generate_user_id)
    name: str = database.Column(database.String(200), nullable = False)
    price: float = database.Column(database.Float(), nullable = False)
    created: datetime = database.Column(database.DateTime(), default = datetime.now)
    updated: datetime = database.Column(database.DateTime(), nullable = True)
    is_bought: bool = database.Column(database.Boolean(), default = False)
    buyer: str | User | None = database.Column(database.ForeignKey('user.id'), nullable = True)

    def buy(self, customer: User):
        self.is_bought = True
        self.buyer = customer

class Seller(User, database.Model): #? Not sure the inheritance will work

    id: str = database.Column(database.String(36), primary_key = True, default = generate_user_id)
    products: str = database.Column(database.String(600), nullable = False)
    userid = database.Column(database.String(), database.ForeignKey('user.id'))

    @property
    def products_list(self):
        return self.products.split(',')[1:]

    @products_list.setter
    def products_list(self, value):
        self.products = ','.join(value)

    def add_product(self, product):
        if self.products:
            self.products += f',{product}'
        else:
            self.products += product

    @staticmethod
    def from_user(user: User) -> "Seller":
        new_seller = Seller(username = user.username, email_address = user.email_address, \
                            age = user.age, gender = user.gender, products_list = []) #type: ignore
        return new_seller

class Cart(database.Model):
    id: str = database.Column(database.String(60), primary_key = True, default = generate_user_id)
    name: str = database.Column(database.String(60), nullable = False)
    products: str = database.Column(database.String(600), default = '')
    creator: str | User | None = database.Column(database.String(400), \
                                                 database.ForeignKey('user.id'))
    @property
    def products_list(self) -> list[str]:
        return self.products.split(',') 

    @products_list.setter
    def products_list(self, value):
        self.products = ','.join(value)
    
    def add_product(self, product):
        if self.products:
            self.products += f',{product}'
        else:
            self.products += product
