from ...v1 import api
from .resources import ProductsListResource, ProductItemResource

api.add_resource(ProductsListResource, "/products")
api.add_resource(ProductItemResource, "/products/<string:productid>")
