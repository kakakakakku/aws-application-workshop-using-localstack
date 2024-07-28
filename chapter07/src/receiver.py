import json
import os

import boto3

if os.environ['ENV'] == 'local':
    s3 = boto3.client('s3', endpoint_url='http://localhost.localstack.cloud:4566')
elif os.environ['ENV'] == 'test':
    s3 = boto3.client('s3', endpoint_url='http://localhost:14566')


def main(event):
    for record in event['Records']:
        print(record)
        body = json.loads(record['body'])
        s3.put_object(
            Bucket='chapter07-bucket',
            Key=f"chapter07/{body['id']}.json",
            Body=record['body'],
        )


def lambda_handler(event, context):
    main(event)
