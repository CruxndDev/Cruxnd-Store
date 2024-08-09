from flask import Blueprint

products_blueprint = Blueprint("products", __name__)

from . import endpoints, resources