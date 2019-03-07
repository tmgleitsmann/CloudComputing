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
NN_addr = "http://127.0.0.1:5000"                               # ! hard coded for now !
get_DN_List_endpoint = "/readOrGetDNList"                       # NN endpoint: Cli POSTs filename and gets DN list
blockbeat_endpoint = "/BB"                                      # NN endpoint: Cli POSTs filename and gets DN list - is this being used?
err = "ERROR"

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


"""
Gets the filename from user. 
POSTS the filename and size to NN and gets DN list returned. 
Uses DN list to send blocks of data to DNs. 
"""
def create_file():

    print("\n------")
    print("WRITE")
    print("------\n")

    # get name of S3 object from user to create in SUFS         ! TODO: validate user input !
    key = input("Enter an S3 object: ")                         # s3 bucket name: dundermifflin-sufs
    bucket = 'dundermifflin-sufs'                               # hard coded for now
    s3obj = s3.Object(bucket, key)                              # var that represents an s3 object

    try:
        s3_obj_str = s3obj.get()['Body'].read().decode('utf-8')     # data from s3 as a string                  !! CHECK IF FILE EXISTS IN S3 !
    except ClientError as ex:
        print("ERROR: ", ex)
        return

    # Save save file name and file size into json object
    filename = key
    size = s3obj.content_length
    file_dict = {"filename": filename, "filesize": size}        # json object with file name and file size
    data_json = json.dumps(file_dict)                           # convert file info dict into json

    # Send json object to NameNode and get DN list back as a response
    print("Sending file info for WRITE to Name Node:")
    print("  - File name: ", filename)
    print("  - File size: ", size, "\n")
    response = POST(data_json, NN_addr)                         # POST the file name and size to NN

    # check if file already exists (if exists, print error and return)
    # if response.content.decode("utf-8").strip("\"\n") == "ERROR":
    if response is err:
        print("ERROR: cannot write ", filename, "because it already exists.")
        return

    # Else, forward block data to each DN in the DN List
    print("File info sent to NN.")
    print("NN returned DN list for file:", filename)
    print("Sending file blocks to DNs...\n")

    my_DN_dict = json.loads(response)  # json.loads(json.loads(response.content.decode("utf-8")))   # DN list as a dict
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
                # print(block_str)
                POST(block_for_DN, dn)                                      # TODO: change this to DN_IP!!!


"""
Takes a file as a string as a parameter. 
Breaks the file into "block-sized" chunks into a list. 
Returns list. 
"""
def get_file_in_blocks(file_str):
    file_in_blocks = []
    for block in range(0, len(file_str), block_size):
        str = file_str[block:block+block_size]
        file_in_blocks.append(str)
    return file_in_blocks


"""
Calls get_DN_list helper function which returns "ERROR" or DN list. 
If DN list returned, get block data from DN in DN list. 
"""
def read_file():

    dn_list, file = get_DN_list()

    if dn_list == "ERROR":
        return

    print("\n--------------------------------------------")
    print("READ FILE: ", file)
    print("--------------------------------------------")

    total_bytes = 0                                                                   # track how many bytes are read

    # create file and save in local directory
    read_file = open(file, "w")

    # for each block in the file, print the DNs that holds this file
    for block in dn_list:
        # get the list of DN nodes
        uncleaned_list = dn_list[block].split(" ")
        ip_list = list(filter(None, uncleaned_list))
        print(block, " --> ", ip_list)

        # loop through each ip in the ip list
        i = 0
        while i < len(ip_list):
            dn = ip_list[i]
            payload = {"blockid": block}
            # payload = "bogusid"
            response = requests.get(dn, params=payload)
            response = response.content.decode("utf-8")
            print(json.loads(response))                     # TESTING HERE
            print("\n\n")

            # if you've looped through all dn and you still don't have the data... err!
            if response == "ERROR" and i == (len(ip_list) - 1):
                print("ERROR: Missing a block of data! Failure of replication factor.")
                return

            # else, you got the data, save and break to get next block
            # extra check here for block id that does not exists on this node?
            else:
                i = i + 1
                print("------------------------------------------------")
                print("Block: ", block)
                print("From data: ", dn)
                print("type(response)", type(response))
                read_file.write(response)
                # print(type(response))
                print("------------------------------------------------")
                total_bytes = total_bytes + len(response)
                break

    read_file.close()
    print("\nRead of file", file, "complete.")
    print("Total bytes from READ: ", total_bytes, "\n")

    # for dn in ip_list:
    #     # get block data from this DN
    #     # payload = {"blockid": block}
    #     payload = "bogusid"
    #     response = requests.get(dn, params=payload)
    #     print(response.content.decode("utf-8").strip("\"\n"), " ", type(response.content.decode("utf-8").strip("\"\n")))
    #     print()
    #     print()


"""
Gets user input for file name. 
POSTS filename to NN. 
Gets and error message or DN list in return from POST. 
return "ERROR" or DN list as dict.
"""
def get_DN_list():

    # TODO: get user input/validate input for which file they want info for
    file = input("Enter the filename: ")                                # enter name of file to get DN list for
    NN_get_DN_list_addr = NN_addr + get_DN_List_endpoint                # addr + "/readOrGetDNList" endpoint in NN
    data_json = {"filename": file}                                      # create the json object to POST
    response = POST(data_json, NN_get_DN_list_addr)                     # POST filename to NN @ "/readOrGetDNList" endpoint

    # if, NN returned an ERROR, print error message and return
    if response == "ERROR":
        print("\nERROR: This file does not exist")
        err = "ERROR"
        return err, file

    # else, print the formatted DN list
    else:
        return json.loads(response), file


"""
Calls get_DN_list helper function which returns "ERROR" or DN list. 
If DN list returned, print it out formatted. 
"""
def print_DN_list():

    dn_list, file = get_DN_list()

    if dn_list != "ERROR":
        print("\n--------------------------------------------")
        print("GET DN LIST FOR FILE: ", file)
        print("--------------------------------------------")

        # for each block in the file, print the DNs that holds this file
        for block in dn_list:
            print(block, " --> ", end="")
            print(dn_list[block])
        print()


def GET():
    blockbeat_endpoint_addr = NN_addr + blockbeat_endpoint
    response = requests.get(blockbeat_endpoint_addr)                    # get the DN list from the NN
    if response.status_code != 200:
        print("GET ERROR ", response)
        return "ERROR"
    else:
        return response.content


def POST(data, addr):
    response = requests.post(addr, json=data)                            # send data in form of JSON to NN
    if response.status_code != 200:
        print("POST ERROR")
        return err
    else:
        return response.content.decode("utf-8")


def main():

    create_file()                                                     # AKA write
    read_file()

    # # print_DN_list()
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
    #         print_DN_list()
    #
    #     else:
    #         break
    #
    # # Quit program
    # bye()


if __name__ == "__main__":
    main()
