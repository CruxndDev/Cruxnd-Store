from flask import Blueprint
from flask_restful import Api

user_blueprint = Blueprint("user", __name__)

from . import endpoints, resources