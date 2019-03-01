'''

Script for creating and deleting EC2 instances.

'''

import boto3

ec2 = boto3.resource('ec2', region_name="us-west-2")


def create_instance(image_id, num_of_instances):

    instances = ec2.create_instances(ImageId=image_id,                          # minitwit AMI = ami-006414247e8b136d1
                                     MinCount=num_of_instances,
                                     MaxCount=num_of_instances,
                                     SecurityGroupIds=['sg-a12b84d7'],
                                     KeyName="CloudComputingKey",               # add name of your .pem file
                                     InstanceType="t3.micro",
                                     InstanceMarketOptions={
                                        'MarketType': 'spot',
                                        'SpotOptions': {
                                            'MaxPrice': '0.012'}})
    print("Instance created!")
    # global my_instances = instances
    return instances


# def get_instances():
#     return my_instances


def terminate_instances(instances):
    ec2.instances.filter(InstanceIds=instances).terminate()
