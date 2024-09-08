from flask import Blueprint
from flask_restful import Api
from ..models import Seller
from flask import jsonify

SUCCESS_RESPONSE = {"message": "Operation Successful"}


api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

from . import users, products, sellers, endpoints

api_blueprint.register_blueprint(users.user_blueprint, url_prefix="/users")
api_blueprint.register_blueprint(products.products_blueprint, url_prefix="/products")
api_blueprint.register_blueprint(sellers.seller_blueprint, url_prefix="/sellers")
