from ...v1 import api
from .resources import SellerItemResource, SellerListResource

api.add_resource(SellerListResource, "/sellers")
api.add_resource(SellerItemResource, "/sellers/<string:sellerid>")
