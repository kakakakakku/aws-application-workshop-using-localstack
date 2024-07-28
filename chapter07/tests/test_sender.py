import json
import re

import pytest
from localstack_utils.localstack import startup_localstack, stop_localstack
from sender import main, sqs


@pytest.fixture(scope='module', autouse=True)
def _setup():
    startup_localstack(gateway_listen='0.0.0.0:14566')

    sqs.create_queue(
        QueueName='chapter07-queue',
        Attributes={
            'ReceiveMessageWaitTimeSeconds': '20',
        },
    )

    yield

    stop_localstack()


def test_main():
    event = {
        'resource': '/',
        'path': '/',
        'httpMethod': 'POST',
    }

    main(event)

    response = sqs.receive_message(
        QueueUrl='http://sqs.ap-northeast-1.localhost.localstack.cloud:14566/000000000000/chapter07-queue',
        MaxNumberOfMessages=10,
    )

    assert 1 == len(response['Messages'])
    body = json.loads(response['Messages'][0]['Body'])
    assert 'id' in body
    assert re.match(r'id\d{4}', body['id'])
