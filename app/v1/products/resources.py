from datetime import datetime
from typing import NoReturn
from flask import request, abort
from flask_restful import Resource
from ...models import Product, database, User
from ...schemas import ProductItemSchema, CreateProductSchema
from app import cache
from marshmallow import ValidationError

SUCCESS_RESPONSE = {"message": "Operation Successful"}
NOT_FOUND = {"message": "Resource not found"}


def check_seller() -> NoReturn | str:
    seller_id = request.args.get('sellerid')

    if not seller_id:
        abort(401, {'message' : "seller id is missing"})
    else:
        return seller_id
        
class ProductsListResource(Resource):

    def get(self):
        # * format = 127.0.0.1:5000/v1/products?name=Apron&isBought=0&min=500&max=6000
        name = request.args.get("name")
        isBought = request.args.get("isBought", type=bool)
        minimum_price = request.args.get("min")
        maximum_price = request.args.get("max")

        query = Product.query

        if name:
            query = query.filter(Product.name.like(f"%{name}%"))

        if isBought:
            query = query.filter(Product.is_bought == isBought)

        if minimum_price:
            query = query.filter(Product.price >= minimum_price)

        if maximum_price:
            query = query.filter(Product.price <= maximum_price)

        all_products = [ProductItemSchema().dump(product) for product in query.all()]
        return {"products": all_products}

    def post(self):
        # * format = 127.0.0.1:5000/v1/products?seller=<aRandomId>
        sellerid = check_seller()
        try:
            new_product = CreateProductSchema().load(request.json)
            new_product.seller = sellerid
            database.session.add(new_product)
            database.session.commit()
        except ValidationError as err:
            abort(400, err.messages)


class ProductItemResource(Resource):

    def get(self, productid):
        retreived_product = Product.query.get_or_404(productid)
        return {"product": ProductItemSchema().dump(retreived_product)}

    def put(self, productid):
        check_seller()
        product_to_update = Product.query.get_or_404(productid)
        try:
            new_product = CreateProductSchema().load(request.json)
            product_to_update.name = new_product.name
            product_to_update.price = new_product.price
            product_to_update.updated = datetime.now()
            database.session.commit()
        except ValidationError as err:
            abort(400, err.messages)

    def delete(self, productid):
        check_seller()
        product_to_delete = Product.query.get_or_404(productid)
        database.session.delete(product_to_delete)
        database.session.commit()
        return SUCCESS_RESPONSE

    def post(self, productid):
        buyer_id = request.args.get("buyer")
        if not buyer_id:
            abort(401, {"message": "Enter a buyerId query parameter"})

        if not User.query.get(buyer_id):
            abort(404, NOT_FOUND)

        product_to_buy = Product.query.get_or_404(productid)
        product_to_buy.is_bought = True
        product_to_buy.buyer = buyer_id
        database.session.commit()
        return SUCCESS_RESPONSE
