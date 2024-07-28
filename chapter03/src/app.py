import json

import boto3

sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')

queue_url = 'http://sqs.ap-northeast-1.localhost.localstack.cloud:4566/000000000000/chapter03-queue'

response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,
)

s3 = boto3.client('s3', endpoint_url='http://localhost:4566')

for message in response.get('Messages', []):
    body = json.loads(message['Body'])
    s3.put_object(
        Bucket='chapter03-bucket',
        Key=f"{body['id']}.json",
        Body=message['Body'],
    )
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle'],
    )
