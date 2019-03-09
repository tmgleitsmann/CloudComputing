from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse, request
import simplejson as json
import threading
import requests
import atexit

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file')

NN_addr = "http://127.0.0.1:5000"
my_addr = "http://127.0.0.1:6000"
localhost = "http://127.0.0.1"    #THIS NEEDS TO CHANGE TO NAME NODE IP
port = "6000"
blockbeat = "/BB"
err_code = 400
err_message = "ERROR"

# Lock to control access to data
dataLock = threading.Lock()
# Thread handler
yourThread = threading.Thread()
# Time between blockbeats
wait_time = 10

my_blocks = {}

class DN_server(Resource):

    def get(self):
        # Get block id sent from client (key = "blockid")
        parser = reqparse.RequestParser()
        parser.add_argument("blockid")                              # Name of key
        args = parser.parse_args()
        blockid = args["blockid"]                                   # Payload from client containing block id

        print("\nClient requested block: ", blockid, " - checking if I have it...", end="")

        with dataLock:
            # If I have the block id, send the data back
            if blockid in my_blocks.keys():
                print("I HAVE block:", blockid, "\n")
                value = my_blocks[blockid]
                return value

            # Else, return ERROR
            else:
                print("I do NOT have block:", blockid, "\n")
                return err_message

    def post(self):

        with dataLock:
            # Write
            a = json.loads(request.data)
            my_blocks.update(a)                                         # Add {"blockid":"data"} to my_blocks dict

            # Test print
            print("I have blocks: ", end="")
            for blockid in my_blocks.keys():
                print(blockid, "  ", end="")
            print()

        # # Send block report
        # response = requests.post(NN_BB_addr, json=block_report)     # Send my blocks as a list to NN
        #
        # if response.status_code != 200:
        #     print("ERROR: Error in sending block report to NN")
        # else:
        #     print("SUCCESS: Sent block report to NN\n")
        # return request.data.decode("utf-8")

    def interrupt():
        global yourThread
        yourThread.cancel()

    def blockBeat():
        # Do initialisation stuff here
        global yourThread
        # Send block report to NN
        with dataLock:
            NN_BB_addr = NN_addr + blockbeat # Address of NN + block beat end point --> "/BB"
            block_report = {"block_report": list(my_blocks.keys())}

        yourThread = threading.Timer(wait_time, blockBeat, ())
        yourThread.start()

    # Initialize blockBeat thread
    blockBeat()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)

api.add_resource(DN_server, "/")

if __name__ == "__main__":
    # Run main program
    app.run(port)
