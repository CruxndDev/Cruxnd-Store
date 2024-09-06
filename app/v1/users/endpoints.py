from ...v1 import api
from .resources import CartListResource, UserItemResource, UserListResource

api.add_resource(UserListResource, '/users')
api.add_resource(UserItemResource, '/users/<string:userid>')
api.add_resource(CartListResource, '/users/<string:userid>/cart')