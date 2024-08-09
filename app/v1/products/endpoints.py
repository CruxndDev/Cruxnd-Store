from ...v1 import api
from .resources import HelloProducts

api.add_resource(HelloProducts, "/products")