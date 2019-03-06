from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, request
import requests
import json
import datetime


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()        # JSON parser
parser.add_argument('file')

# NN's storage
# beat block lists and
# DN lists

# Temp variables
DN_IP = ["http://127.0.0.1:6000", "http://127.0.0.1:6001", "http://127.0.0.1:6002"]#, "127.0.0.1:6003", "127.0.0.1:6004"]    # temp list of DN IPs -- FIX to heart beat list
master_DNlists_dict = {}                                                # master list of all DN lists
master_heartbeat_dict = {}

# NN Setup
block_size = 4000                                                         # TODO: change from B to MB
replication_factor = 2


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


class BlockBeats(Resource):

    def get(self):
        return "GET response from BlockBeats class"

    def post(self):

        bb = json.loads(request.data.decode("utf-8"))           # list of block id from a DN
        sender_addr = bb["DN_addr"]                             # sender's address (IP + port)
        block_list = bb["block_report"]                         # get list of blocks that this DN currently has

        # update master heart beat list with DN's IP and current time stamp
        master_heartbeat_dict.update({sender_addr: datetime.datetime.now()})

        print("From sender ", sender_addr, " -->  ", block_list)

# WORKING HERE!
#         for blockid_from_dn in block_list:
#             print("block: ", blockid_from_dn)
#             for file in master_DNlists_dict:
#                 for blockid in master_DNlists_dict[file]:
#                     addr_list = master_DNlists_dict[file][blockid]
#                     print(str(blockid), " ", addr_list)
#
#                     if blockid == blockid_from_dn:#sender_addr not in addr_list and blockid == blockid_from_dn:
#                         print("adding ", blockid, " to ", blockid_from_dn)
#                         master_DNlists_dict[file][blockid].append(sender_addr)
#




                    #     # if (blockid == blockid_from_dn) and (sender_addr not in master_DNlists_dict[file][blockid]):
                    #     print("adding ", sender_addr, " to block ", blockid)
                    #     addr_list.append(sender_addr)

            # print("got this block id ", blockid, " from ", sender_addr)
            # filename = blockid[:blockid.find("_b")]
            # block_list_for_this_file = master_DNlists_dict[filename]        # give you
            # dn_list = block_list_for_this_file[blockid]
            # if sender_addr not in dn_list:
            #     dn_list.append(sender_addr)

            # for dn_list in block_list_for_this_file:
            #     for dn in dn_list:
            #         if str(dn) == str(blockid):
            #             if sender_addr not in dn_list:
            #                 dn_list.append(sender_addr)

            # dn_list_for_this_block = block_list_for_this_file[blockid]
            # if sender_addr not in dn_list_for_this_block:
            #     dn_list_for_this_block.append(sender_addr)
            # # print(block_list_for_this_file)
            # print(dn_list_for_this_block)
            # print()


        # save data into master DN list
        # for block in block_list:
        #     heartbeat_data = {block: datetime.datetime.now()}
        #     master_heartbeat_dict.update(heartbeat_data)


        # print("\n*** MASTER DN LIST ***")
        # # print(master_DNlists_dict)
        # print (master_DNlists_dict)
        # print()

        # for key in master_DNlists_dict.keys():
        #     print("-- FILE: ", key)
        #     for block in master_DNlists_dict[key]:
        #         print(block, " ", master_DNlists_dict[key][block])
        #         print()
        # print()
        #
        # print("master HB list: ")
        # for key in master_heartbeat_dict.keys():
        #     print(key, ": ", master_heartbeat_dict[key])


api.add_resource(NN_server, "/")
api.add_resource(BlockBeats, "/BB")


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