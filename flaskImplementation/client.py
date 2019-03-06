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

    # get name of S3 object to create in SUFS -- TODO: validate user input
    # bucket = input("Enter an S3 object: ")                    # s3 bucket name: dundermifflin-sufs
    bucket = 'dundermifflin-sufs'                               # hard coded for now
    key = 'sample_us.tsv'                                       # hard coded for now - this is the only file in the bucket now
    s3obj = s3.Object(bucket, key)                              # var that represents an s3 object
    s3_obj_str = s3obj.get()['Body'].read().decode('utf-8')     # data from s3 as a string

    # Save save file name and file size into json object
    filename = key
    size = s3obj.content_length
    key = filename
    file_dict = {"filename": filename,"filesize": size}
    data_json = json.dumps(file_dict)                           # convert file info dict into json

    print("Sending file info for WRITE to Name Node:")
    print("  - File name: ", filename)
    print("  - File size: ", size, "\n")

    # Send json object to NameNode and get DN list back as a response
    response = POST(data_json, NN_addr)                         # POST the file name and size to NN

# WORKING HERE!
    # check if file already exists (if exists, print error and return)
    if response == "ERROR":
        print("ERROR: cannot write ", filename, "because it already exists.")
        return
    print("Received DN list from NN for file ", filename, "\n")

    # Forward block data to each DN in the DN List
    my_DN_dict = json.loads(json.loads(response.content.decode("utf-8")))   # DN list as a dict
    print("PRINT RECEIVED DN LIST")
    list_data_node(my_DN_dict)                                    # print

    file_in_blocks = get_file_in_blocks(s3_obj_str)  # list of file contents in 64B strings
    i = 0  # index of file_in_blocks

    for f in my_DN_dict:
        for b in my_DN_dict[f]:
            print("Sending block ", b, "to data nodes: ")
            block_str = file_in_blocks[i]                           # get next chunk of file (each chunk = blocked size)
            i = i + 1
            dn_dest_list = my_DN_dict[f][b].strip(" ").split(" ")
            for dn in dn_dest_list:
                block_for_DN = json.dumps({b: block_str})         # convert string to json
                print(dn, " ---> ", end = '')                       # dn represents the ip:port of DN
                print(b)#(json.loads(block_for_DN))
                # print("\n", block_for_DN, "\n")
                POST(block_for_DN, dn)                              # TODO: change this to DN_IP!!!


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


def list_data_node(DN_list_dict):

    # TODO: get user input/validate input for which file they want info for

    for filename in DN_list_dict:                              # this should only loop ONCE
        print("--------------------------------------------")
        print("GET DN LIST FOR FILE: ", filename)
        print("--------------------------------------------")

        for block in DN_list_dict[filename]:
            print(block, " --> ", end="")
            print(DN_list_dict[filename][block])
        print()


def GET():
    response = requests.get("http://127.0.0.1:5000/BB")         # get the DN list from the NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    else:
        return response.content
        # print(response.content)
        # return response.json()
        # print(response.json())


def POST(data, addr):
    response = requests.post(addr, json=data)                   # send data in form of JSON to NN
    if response.status_code != 200:
        print("POST ERROR ", response)
        return "ERROR"
    else:
        return response


def main():

    create_file()                                               # AKA write

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


    # print("calling GET()...")
    # response = GET()
    # dn_list = json.loads(response.decode("utf-8"))
    # # print(dn_list)
    # # print(type(dn_list))
    # blist = ["sample_us.tsv_b0",  "test.txt_b0"]
    #
    # for b in blist:
    #     for f in dn_list:
    #         for bid in dn_list[f]:
    #             if bid == b and bid not in dn_list[f][bid]:
    #                 dn_list[f][bid].append(b)
    #
    # for filename in dn_list:
    #     print("filename: ", filename, " (", type(filename), ")")
    #     for block in dn_list[filename]:
    #         print("\tblock: ", block, " (", type(block), ")")
    #         print("\tlist: ", dn_list[filename][block], " (", type(dn_list[filename][block]), ")")



    #
    # print("calling PUT_to_NN()...")
    # PUT_to_NN()


if __name__ == "__main__":
    main()

