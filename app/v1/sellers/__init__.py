from flask import Blueprint

seller_blueprint = Blueprint('sellers', __name__)

from . import endpoints, resources