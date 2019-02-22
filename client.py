'''
Outline for client program (See page 5 of assignment page)
Q: ask prof L if actions are correct
'''


def greetings():
    print("\n---------------------------------------------")
    print("Welcome to the Dunder Mifflin Client Program!")
    print("---------------------------------------------\n")


def bye():
    print("\nThanks for Dunder Mifflin. Bye!\n")


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
    # TODO: get user input/validate input for which s3 object to use. (Data from this s3 obj written into file)
    # Do we need to get file size from user? Or is file size with s3 object?


def read_file():
    print("\nTo implement: Read file...\n")
    # TODO: get user input/validate input for which filename user wants to read
    # TODO: send file name to NN
    # TODO: Receive copy of file from NN


def list_data_node():
    print("\nTo implement: Listing data nodes that store replicas of each block of file...\n")
    # TODO: get user input/validate input for which file they want info for


def main():

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
