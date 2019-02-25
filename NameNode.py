'''

Outline for Data Node

'''

import boto3
ec2 = boto3.resource('ec2', region_name="us-west-2")

instances = ec2.create_instances(ImageId='ami-006414247e8b136d1',
                                 MinCount=1,
                                 MaxCount=1,
                                 SecurityGroupIds=['sg-a12b84d7'],
                                 KeyName="",                        # add name of your .pem file
                                 InstanceType="t3.micro",
                                 InstanceMarketOptions={
                                    'MarketType': 'spot',
                                    'SpotOptions': {
                                        'MaxPrice': '0.012'}})
