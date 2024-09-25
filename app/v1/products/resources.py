from datetime import datetime
from flask import request, abort
from flask_restful import Resource
from ...models import Product, Seller, database, User, add_productid
from ...schemas import ProductItemSchema, CreateProductSchema
from marshmallow import ValidationError

SUCCESS_RESPONSE = {"message": "Operation Successful"}
NOT_FOUND = {"message": "Resource not found"}


def check_seller():
    seller_id = request.args.get("sellerId")

    if not seller_id:
        abort(400, {"message": "seller id is missing"})
    else:
        return Seller.query.get(seller_id)

class ProductsListResource(Resource):

    def get(self):
        # * format = 127.0.0.1:5000/v1/products?name=Apron&isBought=0&min=500&max=6000
        name = request.args.get("name")
        isBought = request.args.get("isBought", type=bool)
        minimum_price = request.args.get("min")
        maximum_price = request.args.get("max")
        current_page = request.args.get("currentPage", type=int, default=1)
        items_per_page = request.args.get("itemsPerPage", type=int, default=10)

        query = Product.query

        if name:
            query = query.filter(Product.name.like(f"%{name}%"))
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

        if isBought:
            query = query.filter(Product.is_bought == isBought)
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

        if minimum_price:
            query = query.filter(Product.price >= minimum_price)
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

        if maximum_price:
            query = query.filter(Product.price <= maximum_price)
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

        pagination = query.paginate(page=current_page, per_page=items_per_page)

        all_products = [
            ProductItemSchema().dump(product) for product in pagination.items
        ]
        return {
            "products": all_products,
            "current_page": pagination.page,
            "no of pages": pagination.pages,
        }

    def post(self):
        # * format = 127.0.0.1:5000/v1/products?seller=<aRandomId>
        try:
            new_product = CreateProductSchema().load(request.json)
            database.session.add(new_product)
            database.session.commit()
            seller = Seller.query.get(new_product.seller)
            add_productid(seller, productid=new_product.id)
            return SUCCESS_RESPONSE, 201
        except ValidationError as err:
            abort(400, err.messages)


class ProductItemResource(Resource):

    def get(self, productid):
        retreived_product = Product.query.get_or_404(productid)
        return {"product": ProductItemSchema().dump(retreived_product)}

    def put(self, productid):
        product_to_update = Product.query.get_or_404(productid)
        try:
            new_product = CreateProductSchema().load(request.json)
            product_to_update.name = new_product.name
            product_to_update.price = new_product.price
            product_to_update.updated = datetime.now()
            database.session.commit()
            return SUCCESS_RESPONSE, 204
        except ValidationError as err:
            abort(400, err.messages)

    def delete(self, productid):
        check_seller()
        product_to_delete = Product.query.get_or_404(productid)
        database.session.delete(product_to_delete)
        database.session.commit()
        return SUCCESS_RESPONSE, 204

    def post(self, productid):
        buyer_id = request.args.get("buyerid")
        if not buyer_id:
            abort(400, {"message": "Enter a buyerId query parameter"})

        if not User.query.get(buyer_id):
            abort(404, NOT_FOUND)

        product_to_buy = Product.query.get_or_404(productid)
        product_to_buy.is_bought = True
        product_to_buy.buyer = buyer_id
        database.session.commit()
        return SUCCESS_RESPONSE, 201
