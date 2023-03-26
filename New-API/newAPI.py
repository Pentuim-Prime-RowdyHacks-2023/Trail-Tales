from flask import Flask
from requests import request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

app = Flask(__name__)
api = Api(app)


resource_fields_USER = {
    "uid": fields.String,
    "firstName": fields.String,
    "lastName": fields.String,
    "userEmail": fields.String
}

class UserTable(Resource):
    @marshal_with(resource_fields_USER)
    def get(self, uid):
        result = 

if __name__ == "__main__":
    app.run(debug=True)