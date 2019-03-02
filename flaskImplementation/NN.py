from flask import Flask             # research
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()        # JSON parser
parser.add_argument('file')

# NN's storage
# beat block lists and
# DN lists

class NN_server(Resource):
    def get(self):
        return "Hello world! This is a GET response"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("filename")         # name of key
        args = parser.parse_args()
        print(args["filename"])
        return args["filename"]


api.add_resource(NN_server, "/")                # do research on this add.resource


if __name__ == "__main__":
    app.run(port='5000')
