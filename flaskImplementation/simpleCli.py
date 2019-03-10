import requests
import boto3
import json
import base64
from flask import request
from os import environ

s3 = boto3.resource('s3')
# local_host = "http://127.0.0.1:4000"  # ! hard coded for now !
server_addr = environ['server_addr']
print("\nSERVER'S ADDR:", server_addr, "\n")


def GET(data):
    if data is None:
        response = requests.get(server_addr, params=data)  # get the DN list from the NN
        if response.status_code != 200:
            print("GET ERROR ", response)
            return "ERROR"
        else:
            return response

    else:
        response = requests.get(server_addr, params=data)  # get the DN list from the NN
        if response.status_code != 200:
            print("GET ERROR ", response)
            return "ERROR"
        else:
            return response


def POST(data):
    response = requests.post(local_host, json=data)  # send data in form of JSON to NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    else:
        return response


def main():

    # TEST GET
    # ---------
    print("\nCalling GET...")
    payload = {"data": "Hello from the client"}
    response = GET(payload)
    print(response.content.decode("utf-8"))


    # TEST POST
    # ---------
    print("\nCalling POST...")
    data = {
        "a": "apple",
        "b": "banana"
    }

    data = json.dumps(data)
    response = POST(data)
    print(response.content.decode("utf-8"))

if __name__ == "__main__":
    main()
