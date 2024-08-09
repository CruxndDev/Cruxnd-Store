from flask_restful import Resource

class HelloUsers(Resource):

    def get(self):
        return {"Hello" : "Users"}