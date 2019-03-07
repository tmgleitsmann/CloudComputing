import boto3

queue_name = 'test6.fifo'

# Create SQS client
sqs = boto3.resource('sqs', region_name='us-west-2')

# implement receive!