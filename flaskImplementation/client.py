import requests

localhost = "http://127.0.0.1"
port = "5000"


def GET_from_NN():
    response = requests.get(localhost + ":" + port)
    if response.status_code != 200:             # is supposed to return a JSON
        print("non 200 response - ERROR")
    else:
        print(response.json())


def PUT_to_NN():
    data = {"filename": "text.txt"}
    response = requests.post(localhost + ":" + port, json=data)
    if response.status_code != 200:             # is supposed to return a JSON
        print("non 200 response - ERROR")
    else:
        print("successfully posted :) ")


def main():
    print ("Hello World!")

    print("calling GET_from_NN()...")
    GET_from_NN()

    print("calling PUT_to_NN()...")
    PUT_to_NN()


if __name__ == "__main__":
    main()
