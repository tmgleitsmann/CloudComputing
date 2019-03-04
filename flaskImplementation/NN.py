from flask import Flask             # research
from flask_restful import Api, Resource, reqparse, request
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
block_size = 64
replication_factor = 3

class NN_server(Resource):

    def get(self):
        return "Hello world! This is a GET response"

    def post(self):
        cli_data = json.loads(json.loads(request.data.decode("utf-8")))
        filename = cli_data["filename"]
        filesize = cli_data["filesize"]

        keys = cli_data.keys()
        print(type(keys))
        if filename in keys:
            print("It exist already!")
        else:
            blocks = []
            block_num = 1
            list = []
            inside = {}
            node = len(DN_IP)
            while filesize > 0:
                filesize = int(filesize) - block_size
                blocks.append(filename + "_b" + str(block_num)) # Write Blocks
                block_num += 1
                count = 0
                list.clear()
                while count != replication_factor:
                    list.append(DN_IP[node]) # Write IP
                    count += 1
                    if node == len(DN_IP):
                        node = 1
                    else:
                        node += 1
                dict = {block: list}
                inside.update(dict)


            response = {filename: inside}
            return(response)


        # parser = reqparse.RequestParser()
        #
        # parser.add_argument("filename")         # name of key
        # args = parser.parse_args()
        # print(args["filename"])
        # return args["filename"]


api.add_resource(NN_server, "/")                # do research on this add.resource


if __name__ == "__main__":
    app.run(port='5000')
