'''

Outline for client program (See page 5 of assignment page)

'''

import boto3
# import botocore.credentials

# Global variables
s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')
block_size = 64                 # 64 MB
replication_factor = 3


def greetings():
    print("\n---------------------------------------------")
    print("Welcome to the Dunder Mifflin Client Program!")
    print("---------------------------------------------\n")


def bye():
    print("\nThanks for visiting Dunder Mifflin. Bye!\n")


def action_list():
    options = """\nChoose an action 1-4:\n
    1: Create file in SUFS
    2: Read file
    3: List Data Nodes that store replicas of each block of file 
    4: Exit program\n"""
    print(options)

    selection = input("Please choose an action 1-4: ")

    while selection not in ('1', '2', '3', '4'):
        selection = input("Please choose an action 1-4: ")

    return selection


def create_file():

    print("\nTo implement: Creating file...\n")

    # get name of S3 object to create in SUFS -- TODO: validate user input
    # bucket = input("Enter an S3 object: ")              # s3 bucket name: dundermifflin-sufs
    bucket = 'dundermifflin-sufs'                       # hard coded for now
    key = 'sample_us.tsv'                               # hard coded for now - this is the only file in the bucket now

    s3obj = s3.Object(bucket, key)                      # var that represents an s3 object
    # data = s3obj.get()['Body'].read().decode('utf-8')
    # print(data)

    # Save file size in bytes
    size = s3obj.content_length

    # Send filename and file size to NameNode

    # Get response from NameNode with block list and DN list -- TODO: handle situation if filename is already in use

    # Forward block data to each DN in the DN List


def read_file():
    print("\nTo implement: Read file...\n")
    # TODO: get user input/validate input for which filename user wants to read
    # TODO: send file name to NN
    # TODO: Receive copy of file from NN


def list_data_node():
    print("\nTo implement: Listing data nodes that store replicas of each block of file...\n")
    # TODO: get user input/validate input for which file they want info for


def main():

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)

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


if __name__ == "__main__":
    main()
