import manageEC2 as ec2


def main():

    image_id = "ami-00f4c37326aa8b976"
    nums_of_instances = 2
    instances = ec2.create_instance(image_id, nums_of_instances)


    # response = input("Type \'yes\' when you are ready to terminate instances: ")
    # ec2.terminate_instances([instances])


if __name__ == "__main__":
    main()
