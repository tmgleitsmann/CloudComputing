from flask import Flask
from flask_restful import Api, Resource, reqparse, request
import json
import requests

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file')

localhost = "http://127.0.0.1" #THIS NEEDS TO CHANGE TO NAME NODE IP
port = "5000"

#NN's storage
#beat block list and
#DN lists
my_blocks = {}
my_keys = []

class DN_server(Resource):

    # def put_to_NN(self, list_of_keys):
    #     response = requests.post(localhost + ":" + port, data=list_of_keys)
    #     if response.status_code != 200:             # is supposed to return a JSON
    #         print("non 200 response - ERROR")
    #         return True
    #     else:
    #         print("successfully posted :) ")
    #         return False

    def get(self):
        str_obj = request.data.decode("utf-8")
        if str_obj in my_blocks.keys():
            print('key found. returning contents')
            value = my_blocks[str_obj]
            return value

        return 400

    def post(self):
        str_obj = request.data.decode("utf-8")
        a = json.loads(str_obj)
        print(a.keys())
        my_blocks.update(a)
        #now we need to send a block report to NN from here.
        my_keys.append(a.keys())

        #THIS IS THE BLOCK REPORT FOR THE NAME NODE
        # response = requests.post(localhost + ":" + port, data=my_keys)
        # if response.status_code != 200:             # is supposed to return a JSON
        #     print("non 200 response - ERROR - did not send block report to NN")
        # else:
        #     print("successfully posted block report to NN :) ")


        print(my_blocks)
        print(my_keys)

        return request.data.decode("utf-8")




api.add_resource(DN_server, "/")

if __name__ == "__main__":
    app.run(port='5000')
