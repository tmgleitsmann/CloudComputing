from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse, request
# import json
import simplejson as json

import requests

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file')

NN_addr = "http://127.0.0.1:5000"
my_addr = "http://127.0.0.1:6000"
localhost = "http://127.0.0.1"                          #THIS NEEDS TO CHANGE TO NAME NODE IP
port = "6000"
blockbeat = "/BB"
err_code = 400
err_message = "ERROR"

my_blocks = {}


class DN_server(Resource):

    def get(self):

        # get block id sent from client (key = "blockid")
        parser = reqparse.RequestParser()
        parser.add_argument("blockid")                              # name of key
        args = parser.parse_args()
        blockid = args["blockid"]                                   # payload from client containing block id

        print("\nClient requested block: ", blockid, " - checking if I have it...", end="")

        # if I have the block id, send the data back
        if blockid in my_blocks.keys():
            print("I HAVE block:", blockid, "\n")
            value = my_blocks[blockid]
            print("SENDING BLOCK DATA: ", value)
            return value

        # else, return ERROR
        else:
            print("I do NOT have block:", blockid, "\n")
            return err_message

    def post(self):

        # WRITE
        # receive data as dict from client
        print("in DN post")
        # print(type(request.data))

        a = json.loads(request.data)    # dict - only keep request.data
        # print("\n", type(a))
        # for item in a:
        #     print()
        #     print(a[item])
        #     print()

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
        # send block report
        response = requests.post(NN_BB_addr, json=block_report)     # send my blocks as a list to NN

        if response.status_code != 200:
            print("ERROR: Error in sending block report to NN")
        else:
            print("SUCCESS: Sent block report to NN\n")
        return request.data.decode("utf-8")


api.add_resource(DN_server, "/")

if __name__ == "__main__":
    app.run(port='6000')
