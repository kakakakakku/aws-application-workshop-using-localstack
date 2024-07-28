import json
import os
import random

import boto3

if os.environ['ENV'] == 'local':
    sqs = boto3.client('sqs', endpoint_url='http://localhost.localstack.cloud:4566')
elif os.environ['ENV'] == 'test':
    sqs = boto3.client('sqs', endpoint_url='http://localhost:14566')


def main(event):
    number = random.randint(0, 9999)
    sqs.send_message(
        QueueUrl='http://sqs.ap-northeast-1.localhost.localstack.cloud:4566/000000000000/chapter07-queue',
        MessageBody=json.dumps(
            {
                'id': f'id{number:04}',
                'body': f'This is message {number:04}.',
            }
        ),
    )

    return {
        'statusCode': 200,
        'body': json.dumps(
            {'id': f'id{number:04}'},
        ),
    }


def lambda_handler(event, context):
    return main(event)
