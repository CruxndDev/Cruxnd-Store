"""
* Models file for store api to handle database structure
"""

from datetime import datetime
from uuid import uuid4
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from app import database

load_dotenv()


def add_productid(table, productid):
    table_name = table.__tablename__
    connection = psycopg2.connect(
        user=os.getenv("DEV_DATABASE_USER"),
        password=os.getenv("DEV_DATABASE_PASSWORD"),
        database=os.getenv("DEV_DATABASE"),
    )

    cursor = connection.cursor()

    update_query = """
            UPDATE {0} SET products = array_append(products, '{1}') WHERE id = '{2}' 
        """.format(
        table_name, productid, table.id
    )
    print(update_query)
    cursor.execute(update_query)
    connection.commit()
    connection.close()


def generate_user_id():
    return str(uuid4())


class User(database.Model):
    """
    A User in the cruxnd store
    """

    __tablename__ = "users"
    id = database.Column(
        database.String(36), primary_key=True, default=generate_user_id
    )
    password_hash = database.Column(database.String(256))
    username = database.Column(database.String(200), nullable=False)
    email_address = database.Column(database.String(300), nullable=False)
    age = database.Column(database.Integer(), nullable=False)
    gender = database.Column(database.String(10), nullable=False)
    created = database.Column(database.DateTime(), default=datetime.now)
    seller = database.relationship("Seller", backref="user")
    carts = database.relationship("Cart", backref="user")
    products_bought = database.relationship("Product", backref="users")

    @property
    def password(self):
        raise AttributeError("Password cant be accessed directly")

    @password.setter
    def password(self, value: str):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, user_input: str):
        return check_password_hash(self.password_hash, user_input)


class Product(database.Model):

    __tablename__ = "products"
    id = database.Column(
        database.String(36), primary_key=True, default=generate_user_id
    )
    name = database.Column(database.String(200), nullable=False)
    price = database.Column(database.Float(), nullable=False)
    created = database.Column(database.DateTime(), default=datetime.now)
    updated = database.Column(database.DateTime(), nullable=True)
    is_bought = database.Column(database.Boolean(), default=False)
    buyer = database.Column(database.ForeignKey("users.id"), nullable=True)
    seller = database.Column(database.String(400), database.ForeignKey("sellers.id"))

    def __repr__(self) -> str:
        return f"Product {self.name}"

    def buy(self, customer: User):
        self.is_bought = True
        self.buyer = customer.id


class Seller(User, database.Model):  # ? Not sure the inheritance will work
    __tablename__ = "sellers"
    id = database.Column(
        database.String(36), primary_key=True, default=generate_user_id
    )
    products = database.Column(database.ARRAY(database.String), default=[])
    balance = database.Column(database.Integer(), nullable=False, default=0)
    userid = database.Column(database.String(), database.ForeignKey("users.id"))
    products_sold = database.relationship("Product", backref="product_seller")

    @staticmethod
    def from_user(user: User) -> "Seller":
        new_seller = Seller(
            username=user.username,
            email_address=user.email_address,
            age=user.age,
            gender=user.gender,
        )
        return new_seller


class Cart(database.Model):

    __tablename__ = "carts"
    id = database.Column(
        database.String(60), primary_key=True, default=generate_user_id
    )
    name = database.Column(database.String(200), nullable=False)
    products = database.Column(database.ARRAY(database.String), default=[])
    creator = database.Column(database.String(600), database.ForeignKey("users.id"))
