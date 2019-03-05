from flask import Flask, jsonify
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
DN_IP = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]    # temp list of DN IPs -- FIX to heart beat list
master_DNlists_dict = {}                                                # master list of all DN lists

# NN Setup
block_size = 64                                                         # TODO: change from B to MB
replication_factor = 3


class NN_server(Resource):

    def get(self):
        return "Hello world! This is a GET response"

    def post(self):

        # temp - change to accessing local DN_list !!
        with open("testNNjson.json", "r") as read_file:
            data = json.load(read_file)
        files_list = data.keys()

        # get file name and size from client
        cli_data = json.loads(json.loads(request.data.decode("utf-8")))
        filename = cli_data['filename']
        filesize = cli_data['filesize']

        # if file already exists, ERROR
        if filename in files_list:
            print("This file already exists!")
            return 400                              # change this... what to actually return?

        # else the file does not exist, create the DN list
        # 1: create list of block ids
        blockid_list = []
        block_index = 0
        for i in range(0, filesize, block_size):
            blockid_list.append(filename + "_b" + str(block_index))
            block_index += 1

        # 2: assign a list of DN to each block (round robin) + create an empty DN list to store locally
        block_json = {}                                 # "inside" json for block data (block id and list of DNs)
        block_json_emptylist = {}                       # empty DN list for NN to store
        rr_index = 0;                                   # round robin index
        empty_list = []                                 # for block_json_emptyList

        for block in blockid_list:                      # make a DN list for each blockid in file
            dn_list = []
            for i in range(0, replication_factor):      # assign N number of DNs per blockid, where N = rep. factor
                ip = DN_IP[(rr_index + i) % len(DN_IP)] # round robin assignment
                dn_list.append(ip)

            rr_index = (rr_index + 1) % len(DN_IP)              # increment the rr_index or wraps back around
            block_json.update({block: dn_list})                 # update block_json for client
            block_json_emptylist.update({block: empty_list})    # update block_json_emptyList to store locally

        # 3: create the final DN list to send to client + store the empty DN list version locally in master DN list
        DN_list_json = {filename: block_json_emptylist}
        master_DNlists_dict.update(DN_list_json)                # store the local version

        DN_list_json_cli =  {filename: block_json}
        print("\nSending DN list to client...")
        return json.dumps(DN_list_json_cli)                     # send the client version



api.add_resource(NN_server, "/")                # do research on this add.resource


if __name__ == "__main__":
    app.run(port='5000')

# master_DNlists_dict.update({filename: DN_list_json})
# print(master_DNlists_dict[filename])
# DN_list_for_get = DN_list_json                  # to send to client for a write
# parser = reqparse.RequestParser()
#
# parser.add_argument("filename")         # name of key
# args = parser.parse_args()
# print(args["filename"])
# return args["filename"]