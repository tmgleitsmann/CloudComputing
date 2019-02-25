import manageEC2 as ec2


def main():

    image_id = "ami-006414247e8b136d1"
    nums_of_instances = 1
    ec2.create_instance(image_id, nums_of_instances)


if __name__ == "__main__":
    main()
