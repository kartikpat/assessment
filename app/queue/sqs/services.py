import boto3

# Get the service resource
sqs = boto3.client('sqs')
 
queueName = 'kartiktest'

response = sqs.get_queue_url(QueueName=queueName)

queueURL = response['QueueUrl']

def sendMessage(body, attributes):
	response = sqs.send_message(
					QueueUrl = queueURL,
					MessageBody = body,
					MessageAttributes=attributes
				)

	return response

def receiveMessage():
	response = sqs.receive_message(
				    QueueUrl=queueURL,
				    MaxNumberOfMessages=10,
				    MessageAttributeNames=[
				        'All'
				    ],
				    VisibilityTimeout=60
				)

	return response

def deleteMessage(receiptHandle):
	sqs.delete_message(
		QueueUrl=queueURL,
		ReceiptHandle=receiptHandle
	)
