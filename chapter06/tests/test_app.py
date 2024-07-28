import json
from http import HTTPStatus

import pytest
from app import main, s3
from localstack_utils.localstack import startup_localstack, stop_localstack


@pytest.fixture(scope='module', autouse=True)
def _setup():
    startup_localstack(gateway_listen='0.0.0.0:14566')

    s3.create_bucket(
        Bucket='chapter06-bucket',
        CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'},
    )

    yield

    stop_localstack()


def test_main():
    event = {
        'Records': [
            {
                'body': json.dumps(
                    {
                        'id': 'id0001',
                        'body': 'This is message 0001.',
                    }
                ),
            }
        ],
    }

    main(event)

    response = s3.head_object(
        Bucket='chapter06-bucket',
        Key='chapter06/id0001.json',
    )
    assert response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.OK.value

    response = s3.get_object(
        Bucket='chapter06-bucket',
        Key='chapter06/id0001.json',
    )
    assert response['Body'].read().decode('utf-8') == '{"id": "id0001", "body": "This is message 0001."}'
