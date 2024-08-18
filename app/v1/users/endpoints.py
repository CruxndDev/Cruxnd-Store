from ...v1 import api
from .resources import UserItemResource, UserListResource

api.add_resource(UserListResource, '/users')
api.add_resource(UserItemResource, '/users/<string:userid>')