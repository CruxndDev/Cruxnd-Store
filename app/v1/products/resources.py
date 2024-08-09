from flask_restful import Resource

class HelloProducts(Resource):

    def get(self):
        return {"Hello" : "Products"}