import boto3

queue_name = 'test6.fifo'

# Create SQS client
sqs = boto3.resource('sqs', region_name='us-west-2')


# Create a SQS queue
queue = sqs.create_queue(QueueName=queue_name, Attributes={'FifoQueue': 'true'})
contents = "Simple String to send"

# print("type of queue: ", type(queue))
# queue_url = queue.get('QueueURL')
# print("URL: ", queue_url)
#
# # get files as string
# # text_file = open("SampleOutput.txt", "r")
# # contents = text_file.read()

# Send message to SQS queue
response = sqs.send_message(
    QueueUrl=queue,
    MessageBody="This is a message"
)

print("message sent!")
