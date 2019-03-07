from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse, request
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()                                       # JSON parser
parser.add_argument('file')


class simple_server(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("data")                              # name of key
        args = parser.parse_args()
        get_data = args["data"]
        print("received on GET: ", get_data)

        data = "This is a GET response."
        return make_response(data.encode(), 200)
        # return "This is a GET response."

    def post(self):
        # bb = json.loads(request.data.decode("utf-8"))           # POST data from DN
        data = "Hello from the server"
        print("\nReceived SimpleCli's POST.", request.data.decode("utf-8"))
        return make_response(data.encode(), 200)
        # return "200 OK"


api.add_resource(simple_server, "/")

if __name__ == "__main__":
    app.run(port='4000')
