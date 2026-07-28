# Chapter 2: Try LocalStack

## Deploy an Amazon SQS Queue

In Chapter 2, let's actually use LocalStack!

First, we use the AWS CLI to deploy an Amazon SQS queue to LocalStack.

Deploying to LocalStack is almost identical to deploying an Amazon SQS queue to a real AWS account with the AWS CLI. The key difference is adding `--endpoint-url http://localhost:4566` to the [`aws sqs create-queue`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sqs/create-queue.html) command so that it points to LocalStack.

Let's run the command.

```sh
$ aws sqs create-queue --endpoint-url http://localhost:4566 \
    --queue-name chapter02-queue \
    --attributes ReceiveMessageWaitTimeSeconds=20
{
    "QueueUrl": "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/chapter02-queue"
}
```

If you see a `QueueUrl` in the output, the Amazon SQS queue has been deployed. Easy, right?

## LocalStack AWS CLI

From here on, to reduce the amount of AWS CLI typing, this workshop uses the [LocalStack AWS CLI](https://github.com/localstack/awscli-local) (the `awslocal` command) instead of the plain AWS CLI (the `aws` command). It is a wrapper around the AWS CLI that automatically adds `--endpoint-url` for you — simply replace `aws` with `awslocal` and everything else stays the same.

Set up the LocalStack AWS CLI:

```sh
$ pip install awscli-local
```

Then use the LocalStack AWS CLI to deploy another Amazon SQS queue.

```sh
$ awslocal sqs create-queue \
    --queue-name chapter02-queue-awslocal \
    --attributes ReceiveMessageWaitTimeSeconds=20
{
    "QueueUrl": "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/chapter02-queue-awslocal"
}
```

Again, if you see a `QueueUrl` in the output, the Amazon SQS queue has been deployed. The command got simpler!

## Verify the Resources

To wrap up Chapter 2, let's use the LocalStack AWS CLI to list the deployed Amazon SQS queues. You should see two queues!

```sh
$ awslocal sqs list-queues
{
    "QueueUrls": [
        "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/chapter02-queue",
        "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/chapter02-queue-awslocal"
    ]
}
```

That's it for Chapter 2! ✋

**Next: [Chapter 3: Work with Amazon SQS and Amazon S3 from Python](03-boto3.md)**
