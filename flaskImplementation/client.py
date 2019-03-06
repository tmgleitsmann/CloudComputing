import requests
import boto3
import json
import pprint
from botocore.exceptions import ClientError


# Global variables
s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')
block_size = 4000                     # MB                      # CHANGE THIS BACK TO 64
replication_factor = 2
NN_addr = "http://127.0.0.1:5000"     # hard coded for now
get_DN_List_endpoint = "/getDNList"
# port = "5000"                       # hard coded for now

# port1 = "6000"
# port2 = "7000"                       # hard coded for now
# port3 = "8000"                       # hard coded for now

# ports = [port1, port2, port3]


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

    # get name of S3 object from user to create in SUFS         ! TODO: validate user input !
    key = input("Enter an S3 object: ")                         # s3 bucket name: dundermifflin-sufs
    bucket = 'dundermifflin-sufs'                               # hard coded for now
    s3obj = s3.Object(bucket, key)                              # var that represents an s3 object
    s3_obj_str = s3obj.get()['Body'].read().decode('utf-8')     # data from s3 as a string

    # Save save file name and file size into json object
    filename = key
    size = s3obj.content_length
    file_dict = {"filename": filename,"filesize": size}         # json object with file name and file size
    data_json = json.dumps(file_dict)                           # convert file info dict into json

    # Send json object to NameNode and get DN list back as a response
    print("Sending file info for WRITE to Name Node:")
    print("  - File name: ", filename)
    print("  - File size: ", size, "\n")
    response = POST(data_json, NN_addr)                         # POST the file name and size to NN

    # check if file already exists (if exists, print error and return)
    if response == "ERROR":
        print("ERROR: cannot write ", filename, "because it already exists.")
        return

    # Else, forward block data to each DN in the DN List
    print("File info sent to NN.")
    print("NN returned DN list for file:", filename)
    print("Sending file blocks to DNs...\n")

    my_DN_dict = json.loads(json.loads(response.content.decode("utf-8")))   # DN list as a dict
    file_in_blocks = get_file_in_blocks(s3_obj_str)                         # list of file contents in block-sized str
    i = 0                                                                   # index of file_in_blocks

    # loop through DN_list and send each block to the given DN
    for f in my_DN_dict:
        for b in my_DN_dict[f]:
            print("\nSending block:", b, "...")
            block_str = file_in_blocks[i]                                   # get next chunk of file
            i = i + 1
            dn_dest_list = my_DN_dict[f][b].strip(" ").split(" ")           # convert DN str to DN list

            # for each DN in the DN list, send {blockid: data}
            for dn in dn_dest_list:
                block_for_DN = json.dumps({b: block_str})                   # convert string to json
                print(dn, " ---> ", b)                                      # dn represents the ip:port of DN
                POST(block_for_DN, dn)                                      # TODO: change this to DN_IP!!!


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

    # TODO: get user input/validate input for which file they want info for
    file = input("Enter the filename: ")                                # enter name of file to get DN list for
    NN_get_DN_list_addr = NN_addr + get_DN_List_endpoint                # specify addr + "/getDNList" endpoint in NN
    data_json = {"filename": file}                                      # create the json object to POST
    response = POST(data_json, NN_get_DN_list_addr)                     # POST file name to NN at "/getDNList" endpoint

    # if, NN returned an ERROR, print error message and return
    if response.content.decode("utf-8").strip("\"\n") == "ERROR":
        print("\nERROR: This file does not exist")
        return

    # else, print the formatted DN list
    else:
        dn_list = json.loads(response.content.decode("utf-8"))          # convert from string to dict
        print("\n--------------------------------------------")
        print("GET DN LIST FOR FILE: ", file)
        print("--------------------------------------------")

        # for each block in the file, print the DNs that holds this file
        for block in dn_list:
            print(block, " --> ", end="")
            print(dn_list[block])
        print()


def GET():
    response = requests.get("http://127.0.0.1:5000/BB")         # get the DN list from the NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    else:
        return response.content


def POST(data, addr):
    response = requests.post(addr, json=data)                   # send data in form of JSON to NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    else:
        return response


def main():

    # create_file()                                               # AKA write

    greetings()

    # Loop until user quits with action #4
    while True:

        # print action selection list
        action = action_list()

        if action is "1":
            create_file()

        elif action is "2":
            read_file()

        elif action is "3":
            list_data_node()

        else:
            break

    # Quit program
    bye()


    # print("calling GET()...")
    # response = GET()

    # print("calling PUT_to_NN()...")
    # PUT_to_NN()


if __name__ == "__main__":
    main()

