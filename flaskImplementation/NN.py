from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse, request
import requests
# import json
import simplejson as json
import datetime

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()                                       # JSON parser
parser.add_argument('file')

# temp list of DN IPs -- FIX to heart beat list
DN_IP = ["http://127.0.0.1:6000", "http://127.0.0.1:6001", "http://127.0.0.1:6002"]

# NN data
master_DNlists_dict = {}                                                # master list of all DN lists
master_heartbeat_dict = {}                                              # master list for block reports / heart beats

# NN Setup
block_size = 64000000                                                   # TODO: change from B to MB
replication_factor = 2
err_code = 400
err_message = "ERROR"

class NN_server(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("filename")                              # name of key
        args = parser.parse_args()
        filename = args["filename"]                                   # payload from client containing block id

        print("\nClient requested file: ", filename, " - checking if I have it...", end="")

        # if I have the file, send the DN list back
        if filename in master_DNlists_dict.keys():
            print("I HAVE file:", filename, "\n")
            dn_list = master_DNlists_dict[filename]
            return dn_list

        # else, return ERROR
        else:
            print("I do NOT have file:", filename, "\n")
            return "ERROR"
    #             # get the file name from POST request
    #         bb = json.loads(request.data.decode("utf-8"))
    #         file = bb["filename"]
    #
    #         # if file exists in my master DN list, return the DN list associated with it
    #         if file in master_DNlists_dict:
    #             return master_DNlists_dict[file]
    #
    #         # else, return error message
    #         else:
    #             return err_message

    def post(self):

        files_list = master_DNlists_dict.keys()

        # get file name and size from client
        print("data from client...")
        cli_data = json.loads(json.loads(request.data.decode("utf-8")))

        # # cli_data = json.loads(json.loads(request.data.decode("utf-8")))
        # print(cli_data)
        # print(type(cli_data))
        filename = cli_data['filename']
        filesize = cli_data['filesize']

        # if file already exists, ERROR
        if filename in files_list:
            print("This file already exists!")
            return make_response(err_message.encode(), err_code)

        # else the file does not exist, create the DN list
        # 1: create list of block ids
        blockid_list = []
        block_index = 0
        for i in range(0, filesize, block_size):
            blockid_list.append(filename + "_b" + str(block_index))
            block_index += 1

        # 2: assign a list of DN to each block (round robin) + create an empty DN list to store locally
        block_json = {}                                     # "inside" json for block data (block id and list of DNs)
        block_json_emptylist = {}                           # empty DN list for NN to store
        rr_index = 0                                        # round robin index
        empty_str = ""                                      # for block_json_emptyList

        for block in blockid_list:                          # make a DN list for each blockid in file
            dn_str = ""
            for i in range(0, replication_factor):          # assign N number of DNs per blockid, where N = rep. factor
                ip = DN_IP[(rr_index + i) % len(DN_IP)]     # round robin assignment
                dn_str = dn_str + ip + " "
                # dn_list.append(ip)

            rr_index = (rr_index + 1) % len(DN_IP)              # increment the rr_index or wraps back around
            block_json.update({block: dn_str})                  # update block_json for client
            block_json_emptylist.update({block: empty_str})     # update block_json_emptyList to store locally

        # 3: create the final DN list to send to client + store the empty DN list version locally in master DN list
        DN_list_json = {filename: block_json_emptylist}
        master_DNlists_dict.update(DN_list_json)                # store the local version

        DN_list_json_cli =  {filename: block_json}

        print("\nSending DN list to client...")
        return make_response(json.dumps(DN_list_json_cli), 200)
        # return json.dumps(DN_list_json_cli)                     # send the client version


class BlockBeats(Resource):

    # def get(self):
    #     return master_DNlists_dict#"GET response from BlockBeats class"

    # For DN's block report / heart beat.
    # DN will POST its address and a list of block ids. Use this info to update master DN list.
    def post(self):

        bb = json.loads(request.data.decode("utf-8"))           # POST data from DN
        sender_addr = bb["DN_addr"]                             # sender's address (IP + port)
        block_list = bb["block_report"]                         # get list of blocks that this DN currently has

        # update master heart beat list with DN's IP and current time stamp
        master_heartbeat_dict.update({sender_addr: datetime.datetime.now()})

        # display who send the block report and what the block report contains
        print("Block report from:", sender_addr)
        print(block_list, "\n")

        # update master DN list
        for dn_b in block_list:
            for f in master_DNlists_dict:
                for b in master_DNlists_dict[f]:
                    ip_list = master_DNlists_dict[f][b].split(" ")
                    if b == dn_b and sender_addr not in ip_list:
                        master_DNlists_dict[f][b] = master_DNlists_dict[f][b] + " " + sender_addr + " "

        print("MASTER LIST")
        for f in master_DNlists_dict:
            print("file: ", f)
            for b in master_DNlists_dict[f]:
                print("\tblock: ", b, " --> ", master_DNlists_dict[f][b])
        print()


# class read_or_get_DN_list(Resource):
#
#     # For client's "get DN list" operation.
#     # Client will POST a file name. If file exists, return DN list. Else, return "ERROR"
#     def post(self):
#
#         # get the file name from POST request
#         bb = json.loads(request.data.decode("utf-8"))
#         file = bb["filename"]
#
#         # if file exists in my master DN list, return the DN list associated with it
#         if file in master_DNlists_dict:
#             return master_DNlists_dict[file]
#
#         # else, return error message
#         else:
#             return err_message


api.add_resource(NN_server, "/")
api.add_resource(BlockBeats, "/BB")
# api.add_resource(read_or_get_DN_list, "/readOrGetDNList")


if __name__ == "__main__":
    app.run(port='5000')
