from flask import Flask, make_response, request
from flask_restful import Api, Resource, reqparse, request
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()                                       # JSON parser
parser.add_argument('file')

# ip = request.environ['REMOTE_ADDR']
# port = request.environ['REMOTE_PORT']
# print(ip, " ", port)

class simple_server(Resource):

    def get(self):
        ip = request.environ['REMOTE_ADDR']
        port = request.environ['REMOTE_PORT']
        print("ON GET: ", ip, " ", port)

        parser = reqparse.RequestParser()
        parser.add_argument("data")                              # name of key
        args = parser.parse_args()
        get_data = args["data"]
        print("received on GET: ", get_data)

        data = "This is a GET response."
        return make_response(data.encode(), 200)

    def post(self):

        ip = request.environ['REMOTE_ADDR']
        port = request.environ['REMOTE_PORT']
        print("ON POST: ", ip, " ", port)

        data = "Hello from the server"
        print("\nReceived SimpleCli's POST.", request.data.decode("utf-8"))
        return make_response(data.encode(), 200)


api.add_resource(simple_server, "/")

if __name__ == "__main__":
    app.run(port='5000')
