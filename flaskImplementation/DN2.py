from flask import Flask
from flask_restful import Api, Resource, reqparse, request
import json
import requests

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file')

NN_addr = "http://127.0.0.1:5000"
my_addr = "http://127.0.0.1:6001"
localhost = "http://127.0.0.1"                          #THIS NEEDS TO CHANGE TO NAME NODE IP
port = "6001"
blockbeat = "/BB"

my_blocks = {}


class DN_server(Resource):

    def get(self):
        str_obj = request.data.decode("utf-8")
        if str_obj in my_blocks.keys():
            print('key found. returning contents')
            value = my_blocks[str_obj]
            return value

        return 400

    def post(self):

        # WRITE
        # receive data as dict from client
        str_obj = request.data.decode("utf-8")
        a = json.loads(json.loads(str_obj))                         # data as a dict
        my_blocks.update(a)                                         # add {"blockid":"data"} to my_blocks dict

        # test print
        print("I have blocks: ", end="")
        for blockid in my_blocks.keys():
            print(blockid, "  ", end="")
        print()

        # Send block report to NN
        NN_BB_addr = NN_addr + blockbeat                            # address of NN + block beat end point --> "/BB"
        block_report = {
            "DN_addr": my_addr,
            "block_report": list(my_blocks.keys())
        }
        response = requests.post(NN_BB_addr, json=block_report)     # send my blocks as a list to NN

        if response.status_code != 200:
            print("ERROR: Error in sending block report to NN")
        else:
            print("SUCCESS: Sent block report to NN\n")
        return request.data.decode("utf-8")


api.add_resource(DN_server, "/")

if __name__ == "__main__":
    app.run(port='6001')
