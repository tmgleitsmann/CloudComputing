import requests
import boto3
import json

s3 = boto3.resource('s3')
local_host = "http://127.0.0.1:4000"  # ! hard coded for now !


def GET(data):
    if data is None:
        response = requests.get(local_host, params=data)  # get the DN list from the NN
        if response.status_code != 200:
            print("GET ERROR ", response)
            return "ERROR"
        else:
            return response

    else:
        response = requests.get(local_host, params=data)  # get the DN list from the NN
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

    # TEST BOTO3 and FORMAT OF DATA
    # ------------------------------
    bucket = 'dundermifflin-sufs'
    key = "sample_us.tsv"
    s3obj = s3.Object(bucket, key)
    s3_obj_str = s3obj.get()['Body'].read().decode('utf-8')                 # TODO: check if file exists
    print(s3_obj_str)
    test_data = json.dumps({"blockid": s3_obj_str})

    # SEND FILE NAME AND FILE SIZE
    # filename = key
    # size = s3obj.content_length
    # file_dict = {"filename": filename, "filesize": size}                    # json object with file name and file size
    # data_json = json.dumps(file_dict)                                       # convert file info dict into json


    # TEST GET
    # ---------
    # print("\nCalling GET...")
    # payload = {"data": "Hello from the client"}
    # response = GET(payload)
    # print(response.content.decode("utf-8"))
    # # print(response.content.decode("utf-8"))


    # TEST POST
    # ---------
    print("\nCalling POST...")
    # data = {
    #     "a": "apple",
    #     "b": "banana"
    # }
    response = POST(test_data)
    print(response.content.decode("utf-8"))

if __name__ == "__main__":
    main()
