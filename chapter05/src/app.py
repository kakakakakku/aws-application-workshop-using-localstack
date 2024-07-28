import json

import boto3

s3 = boto3.client('s3', endpoint_url='http://localhost.localstack.cloud:4566')


def lambda_handler(event, context):
    for record in event['Records']:
        print(record)
        body = json.loads(record['body'])
        s3.put_object(
            Bucket='chapter05-bucket',
            Key=f"{body['id']}.json",
            Body=record['body'],
        )
