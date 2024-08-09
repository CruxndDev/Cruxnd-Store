from flask import Blueprint
from flask_restful import Api


api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

from . import users, products
api_blueprint.register_blueprint(users.user_blueprint, url_prefix = '/users')
api_blueprint.register_blueprint(products.products_blueprint, url_prefix = '/products')