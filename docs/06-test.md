# Chapter 6: Run Unit Tests with a Disposable LocalStack

## Unit Tests

We deployed an AWS Lambda function in Chapter 5. In real-world development, when you modify the function's code you could deploy it to LocalStack without any verification — but ideally you want to run unit tests first and deploy with confidence! In Chapter 6, we combine **pytest** with LocalStack to run unit tests for Python code.

See the [pytest documentation](https://docs.pytest.org/en/stable/) for details.

## localstack-utils

Running unit tests requires a LocalStack instance dedicated to testing.

You would typically start that test LocalStack on a port other than the default `4566`, which means extra steps to start and stop LocalStack both locally and in CI environments such as GitHub Actions. Moreover, the test LocalStack should be immutable — reset for every test run.

In this chapter, we use [**localstack-utils**](https://docs.localstack.cloud/aws/customization/integrations/localstack-sdks/testing-utils/), provided by LocalStack, to start a **disposable** LocalStack instance during test execution.

## Run the Unit Tests

Run the following commands to set up the test environment. `src/requirements.txt` lists the packages the AWS Lambda function code depends on, and `tests/requirements-test.txt` lists the packages the unit tests depend on.

> [!NOTE]
> If you would like to understand the code before running it, read the "Code Walkthrough" section at the end of this chapter first, then come back here.

```sh
$ cd ${CODESPACE_VSCODE_FOLDER}/chapter06
$ pip install -r src/requirements.txt
$ pip install -r tests/requirements-test.txt
```

Then run the unit tests with the following command. The test code is in `chapter06/tests/test_app.py`. It executes the code that the AWS Lambda function runs and checks that an object is saved to the Amazon S3 bucket as expected.

```sh
$ ENV=test python -m pytest -p no:warnings --verbose

FAILED tests/test_app.py::test_main - botocore.exceptions.ClientError: An error occurred (404) when calling the HeadObject operation: Not Found
```

> [!NOTE]
> The unit test is designed to fail intentionally.

You should see **FAILED tests/test_app.py::test_main** — the unit test failed. Don't worry, that is expected!

## Fix the Python Code

In Chapters 3 and 5, objects such as `id0001.json` were saved directly at the root of the Amazon S3 bucket. In Chapter 6, we want to change the specification so that objects are saved under a `chapter06` folder. The test code already reflects this expected specification — that is why the unit test failed.

Open `chapter06/src/app.py` in GitHub Codespaces and modify the Python code as follows.

```diff python
-Key=f"{body['id']}.json",
+Key=f"chapter06/{body['id']}.json",
```

## Run the Unit Tests Again

Let's run the unit tests one more time!

```sh
$ ENV=test python -m pytest -p no:warnings --verbose

tests/test_app.py::test_main PASSED
```

If you see `PASSED`, it worked!

The key point of this unit test is that it starts a **disposable** LocalStack first, runs the test, and removes the LocalStack instance afterward. With **localstack-utils**, you can manage the LocalStack lifecycle inside your test code and run tests repeatedly, both locally and in CI environments such as GitHub Actions.

## Deploy the Serverless Application

Now deploy the serverless application containing the fixed Python code with the `samlocal` command, the same way as in Chapter 5.

```sh
$ samlocal build
$ samlocal deploy

Successfully created/updated stack - chapter06-stack in us-east-1
```

If you see `Successfully created/updated stack - chapter06-stack`, it worked!

## Run the Serverless Application

Just like in Chapter 5, send a message to the Amazon SQS queue with the `awslocal` command. The expectation: sending a message to the queue automatically triggers the AWS Lambda function, which saves an object to the Amazon S3 bucket — this time under the `chapter06` folder. The message is the JSON string `{ "id": "id0004", "body": "This is message 0004." }`.

```sh
$ awslocal sqs send-message \
    --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/chapter06-queue \
    --message-body '{ "id": "id0004", "body": "This is message 0004." }'
```

## Verify the Resources

Let's use the LocalStack AWS CLI to check the deployed resources!

```sh
$ awslocal s3 ls s3://chapter06-bucket --recursive
2026-07-27 00:00:00         49 chapter06/id0004.json
```

The `chapter06/id0004.json` object has been saved to the Amazon S3 bucket!

That's it for Chapter 6! ✋

## Code Walkthrough

Here is a quick walkthrough of the key points in the code. Feel free to skip this section.

### `src/app.py`

The code looks similar to Chapter 5, but there are two significant differences.

First, the logic that used to live in the `lambda_handler()` function has been moved into a `main()` function.

```python
def main(event):
    for record in event['Records']:
        print(record)
        body = json.loads(record['body'])
        s3.put_object(
            Bucket='chapter06-bucket',
            Key=f"{body['id']}.json",
            Body=record['body'],
        )


def lambda_handler(event, context):
    main(event)
```

Why? The AWS Lambda [best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) include the technique "Separate the Lambda handler from your core logic," which makes the code easier to run locally and in unit tests.

The second difference is how the Amazon S3 client is initialized. The `ENV` environment variable switches between the local environment (`local`) and the test environment (`test`), so the code can connect to different LocalStack instances.

```python
if os.environ['ENV'] == 'local':
    s3 = boto3.client('s3', endpoint_url='http://localhost.localstack.cloud:4566')
elif os.environ['ENV'] == 'test':
    s3 = boto3.client('s3', endpoint_url='http://localhost:14566')
```

This workshop never touches a real AWS account, but if you use this pattern at work, initialize the Amazon S3 client without `endpoint_url` for any environment other than local and test, like this:

```python
if os.environ['ENV'] == 'local':
    s3 = boto3.client('s3', endpoint_url='http://localhost.localstack.cloud:4566')
elif os.environ['ENV'] == 'test':
    s3 = boto3.client('s3', endpoint_url='http://localhost:14566')
else:
    s3 = boto3.client('s3')
```

### `tests/test_app.py`

In the test code, a pytest fixture builds the test environment: it calls the localstack-utils `startup_localstack()` function to start LocalStack, deploys an Amazon S3 bucket to the test LocalStack, and runs the test. Finally, it calls the localstack-utils `stop_localstack()` function to stop LocalStack. This is how the disposable LocalStack is implemented.

Note that localstack-utils uses the `latest` Docker image tag by default, but because of the license change introduced in Chapter 1, the `latest` image cannot start without an auth token. That is why `image_name` explicitly points to the v4.14.0 image.

```python
@pytest.fixture(scope='module', autouse=True)
def _setup():
    startup_localstack(
        image_name='localstack/localstack:4.14.0',
        gateway_listen='0.0.0.0:14566',
    )

    s3.create_bucket(
        Bucket='chapter06-bucket',
    )

    yield

    stop_localstack()
```

That's it for the code walkthrough.

**Next: [Chapter 7: Deploy an API with Amazon API Gateway](07-api.md)**
