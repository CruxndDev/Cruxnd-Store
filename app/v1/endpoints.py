from ..models import Seller
from ..v1 import api_blueprint, SUCCESS_RESPONSE
from flask import jsonify


# * Controler Resources
@api_blueprint.route("/sellers/<string:sellerid>/withdraw")
def withdraw(sellerid):
    seller_to_retrieve = Seller.query.get_or_404(sellerid)
    # * Perform stripe based operations
    return 200, jsonify(SUCCESS_RESPONSE)
