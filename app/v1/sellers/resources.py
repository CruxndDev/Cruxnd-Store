from flask_restful import Resource
from flask import jsonify
from ...models import Seller, database
from ...schemas import SellerItemSchema

SUCCESS_RESPONSE = {"message": "Operation Successful"}
NOT_FOUND = {"message": "Resource not found"}


class SellerListResource(Resource):

    def get(self):
        all_sellers = [SellerItemSchema().dump(seller) for seller in Seller.query.all()]
        return {"sellers": all_sellers}


class SellerItemResource(Resource):

    def get(self, sellerid):
        seller_to_retrieve = Seller.query.get_or_404(sellerid)
        return {"seller": SellerItemSchema().dump(seller_to_retrieve)}

    def delete(self, sellerid):
        seller_to_retrieve = Seller.query.get_or_404(sellerid)
        database.session.delete(seller_to_retrieve)
        database.session.commit
        return 200, SUCCESS_RESPONSE
