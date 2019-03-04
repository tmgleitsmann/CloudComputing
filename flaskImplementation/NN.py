from flask import Flask             # research
from flask_restful import Api, Resource, reqparse
import requests
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()        # JSON parser
parser.add_argument('file')

# NN's storage
# beat block lists and
# DN lists

# Temp variables
DN_IP = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]

# NN Setup
replication_factor = 3
node = len(DN_IP)
block_size = 64


# Open json like this?
with open("data_file.json", "r") as read_file:
    data = json.load(read_file)


# Idk how these class/def things work
size = data["filesize"]
response = []
while size > 0:
    size = size - block_size
    response.append(DN_IP[node]) # TODO
    if node = len(DN_IP):
        node = 1
    else
        node += 1
reply to client with json.dumps(response) # TODO



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
