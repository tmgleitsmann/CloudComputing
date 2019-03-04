import requests
import boto3
import json
import pprint


# Global variables
s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')
block_size = 64                     # MB
replication_factor = 3
NN_IP = "http://127.0.0.1"          # hard coded for now
port = "5000"                       # hard coded for now


def greetings():
    print("\n---------------------------------------------")
    print("Welcome to the Dunder Mifflin Client Program!")
    print("---------------------------------------------\n")


def bye():
    print("\nThanks for visiting Dunder Mifflin. Bye!\n")


def action_list():
    options = """\nChoose an action 1-4:\n
    1: Create/write file in SUFS
    2: Read file
    3: List Data Nodes that store replicas of each block of file
    4: Exit program\n"""
    print(options)

    selection = input("Please choose an action 1-4: ")

    while selection not in ('1', '2', '3', '4'):
        selection = input("Please choose an action 1-4: ")

    return selection


def create_file():

    print("\n------")
    print("WRITE")
    print("------\n")

    # get name of S3 object to create in SUFS -- TODO: validate user input
    # bucket = input("Enter an S3 object: ")                # s3 bucket name: dundermifflin-sufs
    bucket = 'dundermifflin-sufs'                           # hard coded for now
    key = 'sample_us.tsv'                                   # hard coded for now - this is the only file in the bucket now
    s3obj = s3.Object(bucket, key)                          # var that represents an s3 object
    s3_obj_str = s3obj.get()['Body'].read().decode('utf-8') # data from s3 as a string

    # Save save file name and file size into json object
    filename = key
    size = s3obj.content_length
    file_dict = {
        "filename": filename,
        "filesize": size
    }
    data_json = json.dumps(file_dict)                       # convert file info dict into json

    # Send json object to NameNode
    POST(data_json, NN_IP)                                  # POST the file name and size to NN
    response = GET()                                        # GET the DN list from the NN
    if response == "ERROR":
        print ("ERROR")
        return
    else:
        print("DN List from NameNode: ")
        print(response, "\n")


    # Get response from NameNode with block list and DN list -- TODO: handle situation if filename is already in use
    # Forward block data to each DN in the DN List
    block_json = response[key]                           # get everything but the filename
    key_list = block_json.keys()                        # list of block names
    file_in_blocks = get_file_in_blocks(s3_obj_str)     # list of file contents in 64B strings
    # print(len)
    i = 0;                                              # index of file_in_blocks

    for key in key_list:
        print("Sending block ", key, "to data nodes: ")
        block_str = file_in_blocks[i]
        i = i + 1

        for dn in block_json[key]:
            block_for_DN = json.dumps({key: block_str})         # convert string to json
            print(dn, " ---> ", end = '')
            print (block_for_DN)
            POST(block_for_DN, NN_IP)                           # TODO: change this to DN_IP!!!
        print("---")


def get_file_in_blocks(file_str):
    file_in_blocks = []
    for block in range(0, len(file_str), block_size):
        str = file_str[block:block+block_size]
        file_in_blocks.append(str)
    return file_in_blocks


def read_file():
    print("\nTo implement: Read file...\n")
    # TODO: get user input/validate input for which filename user wants to read
    # TODO: send file name to NN
    # TODO: Receive copy of file from NN


def list_data_node():
    print("\nTo implement: Listing data nodes that store replicas of each block of file...\n")
    # TODO: get user input/validate input for which file they want info for

    # print("\File: ", key)         # where the key is the filename
    # for key in key_list:
    #     print(key,": " , end = '')
    #     for dn in block_json[key]:
    #         print(dn, " ", end = '')
    #     print()
    # print("\n")


def GET():
    response = requests.get(NN_IP + ":" + port)             # get the DN list from the NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    else:
        return response.json()
        # print(response.json())


def POST(data, IP):
    response = requests.post(IP + ":" + port, json=data)    # send data in form of JSON to NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    # else:
    #     print("Successfully posted :) ")


def main():

    create_file()

    # greetings()
    #
    # # Loop until user quits with action #4
    # while True:
    #
    #     # print action selection list
    #     action = action_list()
    #
    #     if action is "1":
    #         create_file()
    #
    #     elif action is "2":
    #         read_file()
    #
    #     elif action is "3":
    #         list_data_node()
    #
    #     else:
    #         break
    #
    # # Quit program
    # bye()


    # print("calling GET_from_NN()...")
    # GET_from_NN()
    #
    # print("calling PUT_to_NN()...")
    # PUT_to_NN()


if __name__ == "__main__":
    main()

