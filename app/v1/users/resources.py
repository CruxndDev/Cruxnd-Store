from datetime import datetime
from flask import abort, request
from flask_restful import Resource
from marshmallow import ValidationError
from ...schemas import  CreateUserSchema, UserItemSchema
from ...models import User, database

SUCCESS_RESPONSE = {"message" : "Operation Successful"}
NOT_FOUND = {"message" : "Resource not found"}

class UserListResource(Resource):

    def get(self):
        
        #* 127.0.0.1:5000/users?name=john&email=john@doe.com

        query = User.query
        name = request.args.get('name')
        email = request.args.get('email')

        if name:
            query = query.filter(User.username.like(f'%{name}%'))
        
        if email:
            query = query.filter(User.email_address.like(f'%{email}%'))
        
        all_users = [UserItemSchema().dump(user) for user in query.all()]
        return {'users' : all_users}
    
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
        return {"user" : UserItemSchema().dump(user)}
    
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