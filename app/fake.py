from faker import Faker
from sqlalchemy.exc import IntegrityError
from .models import Cart, Seller, User, Product,  database
import random
from datetime import datetime

f = Faker()
products_list = open('app/product_names.txt').readlines()

def create_users():
    count = 0
    while count < 500:
        new_user = User(password = ''.join(f.random_letters(length= 16)), username = f.first_name(), email_address = f.email(), age = f.random_int(20, 40), gender = random.choice(["Male", "Female"]), created = f.date_between(datetime(1980, 1, 1, 0, 0, 0), datetime.today()))

        try:
            database.session.add(new_user)
            database.session.commit()
            count += 1
        except IntegrityError as err:
            print(err._message)
            database.session.rollback()
            continue

def generate_random_user():
    users = User.query.all()
    return random.choice(users)

def generate_random_seller():
    sellers = Seller.query.all()
    return random.choice(sellers)



def create_sellers():
    count = 0
    while count < 50:
        new_seller = Seller.from_user(generate_random_user())

        try:
            database.session.add(new_seller)
            database.session.commit()
            count += 1
        except IntegrityError as err:
            print(err._message)
            database.session.rollback()
            continue
        
def create_products():
    count = 0
    while count < 1000:
        new_product = Product(name = random.choice(products_list), price = random.randrange(0, 50000, 500), created = f.date_time_between(datetime(1980, 1, 1, 0, 0, 0), datetime.today()))
        
        if random.randint(0, 1):
            new_product.buy(generate_random_user())

        try:
            seller = generate_random_seller()
            database.session.add(new_product)
            database.session.commit()
            seller.add_product(new_product.id)
            new_product.seller = seller.id
            count += 1 
        except IntegrityError as err:
            print(err._message)
            database.session.rollback()
            continue

def create_carts():
    count = 0
    while count < 50:
        product_length = random.randint(5, 10)
        new_cart = Cart(name = f.word(), products_list = random.choices([product.id for product in Product.query.all()], k = product_length), creator = generate_random_user().id)
    
        try:
            database.session.add(new_cart)
            database.session.commit()
            count += 1
        except IntegrityError as err:
            print(err._message)
            database.session.rollback()
            continue