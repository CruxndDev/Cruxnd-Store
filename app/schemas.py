from marshmallow import Schema, fields, post_load, post_dump
from .models import Cart, Product, Seller, User
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_URL = os.getenv('SERVER_URL')

class CreateUserSchema(Schema):
    username = fields.String(required = True)
    email_address = fields.Email(required = True)
    age = fields.Integer(required = True)
    password = fields.String(required = True, load_only = True)
    gender = fields.String(required = True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class UserItemSchema(CreateUserSchema, Schema):
    id = fields.String(required = True)
    created = fields.DateTime(required = True, dump_only = True)
    last_online = fields.DateTime(required = True, dump_only = True)

class CreateProductSchema(Schema):
    name = fields.String(required = True)
    price = fields.Float(required = True)

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)

class ProductItemSchema(CreateProductSchema, Schema):
    id = fields.String(required = True)
    created = fields.DateTime(required = True, dump_only = True)
    updated = fields.DateTime(required = True, dump_only = True)
    is_bought = fields.Boolean(required = True, dump_only = True)
    buyer = fields.String(required = False)
    
    @post_dump
    def make_product_items(self, mapping, **kwargs):
        if mapping['is_bought']:
            mapping['buyer'] = '{0}users/{1}'.format(SERVER_URL, mapping['buyer'])
        
        mapping['url'] = '{0}products/{1}'.format(SERVER_URL, mapping['id'])
        return mapping


class SellerItemSchema(UserItemSchema, Schema):
    balance = fields.String(required = True)
    products_list = fields.List(fields.String(), required = True, dump_only = True)
    
    @post_load
    def make_seller(self, data, **kwargs):
        return Seller(**data)

class CreateCartSchema(Schema):
    products_list = fields.List(fields.String(), required = True)

    @post_load
    def make_cart(self, data, **kwargs):
        return Cart(**data)

class CartItemSchema(CreateCartSchema, Schema):
    owner = fields.String(required = True)
    created = fields.DateTime(dump_only = True)