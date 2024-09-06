from datetime import datetime
from flask import abort, request
from flask_restful import Resource
from marshmallow import ValidationError
from ...schemas import CreateUserSchema, UserItemSchema, CartItemSchema
from ...models import User, database, Cart

SUCCESS_RESPONSE = {"message": "Operation Successful"}
NOT_FOUND = {"message": "Resource not found"}
ERROR_RESPONSE = {"message": "Operation not allowed"}


class UserListResource(Resource):

    def get(self):
        """
        * 127.0.0.1:5000/users?name=john&email=john@doe.com'
        username = username
        email_address = emailAddress
        current_page = currentPage
        items_per_page = itemsPerPage
        """

        query = User.query
        username = request.args.get("username")
        email_address = request.args.get("emailAddress")
        current_page = request.args.get("currentPage", type = int, default = 1)
        items_per_page = request.args.get("itemsPerPage", type = int, default = 10)

        if username and email_address:
            return ERROR_RESPONSE, 400

        if username:
            query = query.filter(User.username.like(f"%{username}%"))
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

        if email_address:
            query = query.filter(User.email_address.like(f"%{email_address}%"))
            pagination = query.paginate(
                page=current_page, per_page=items_per_page, error_out=True
            )

        pagination = query.paginate(page=current_page, per_page=items_per_page)

        all_users = [UserItemSchema().dump(user) for user in pagination.items]
        return {
            "users": all_users,
            "current_page": pagination.page,
            "no of pages": pagination.pages,
        }

    def post(self):

        try:
            new_user = CreateUserSchema().load(request.json)
            database.session.add(new_user)
            database.session.commit()
            return SUCCESS_RESPONSE, 201

        except ValidationError as err:
            return err.messages, 401


class UserItemResource(Resource):

    def get(self, userid):
        user = User.query.get_or_404(userid)
        return {"user": UserItemSchema().dump(user)}

    def put(self, userid):
        user_to_update = User.query.get_or_404(userid)

        try:
            new_user = CreateUserSchema().load(request.json)
            user_to_update.username = new_user.username
            user_to_update.email_address = new_user.email_address
            user_to_update.gender = new_user.gender
            user_to_update.updated = datetime.now()
            database.session.commit()
            return SUCCESS_RESPONSE, 200
        except ValidationError as err:
            abort(400, err.messages)

    def delete(self, userid):
        user_to_delete = User.query.get_or_404(userid)
        database.session.delete(user_to_delete)
        database.session.commit()
        return SUCCESS_RESPONSE, 200


class CartListResource(Resource):

    def get(self, userid):
        user_to_get = User.query.get_or_404(userid)
        cart = user_to_get.carts[0]

        return {"cart": CartItemSchema().dump(cart)}

    def post(self, userid):
        productid = request.args.get("productid", type=str)

        if not productid:
            abort(404, {"Message": "enter a product id"})

        user_to_get = User.query.get_or_404(userid)

        if not user_to_get.carts:
            new_cart = Cart(
                name=f"{user_to_get} cart", creator=user_to_get
            )

            database.session.add(new_cart)
            database.session.commit()

            new_cart.add_product(productid)
            return SUCCESS_RESPONSE, 200

        if productid not in cart.products_list:
            cart = user_to_get.carts[0]
            cart.add_product(productid)
            database.session.commit()
            return SUCCESS_RESPONSE, 200

        return {"message": "Item already in cart"}, 400
