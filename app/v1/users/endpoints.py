from ...v1 import api
from .resources import HelloUsers

api.add_resource(HelloUsers, "/users")