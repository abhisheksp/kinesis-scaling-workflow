# Kinesis Scaling Workflow

Simple Step Function to scale up/down your Kinesis Data Stream shard to the desired shard count.

# Why?

Current Limitation of one single Kinesis Shard Update operation:

* Cannot scale up to more than double your current shard count for a stream
* Cannot scale down below half your current shard count for a stream

In order to scale up or scale down your shards beyond the double/half thresholds, you need to perform multiple update
shard operations and wait in between. This package offers a simple step function to automate these steps.

Ref: [Update Shard Count Doc](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_UpdateShardCount.html)

PS: I also wanted to try out the relatively new AWS SDK integrations from AWS Step
Functions[Ref: [Announcement](https://aws.amazon.com/about-aws/whats-new/2021/09/aws-step-functions-200-aws-sdk-integration/)]

# CDK Deployment Steps

This packages uses AWS CDK to define and deploy infrastructure which includes a Lambda and a Step Function State
Machine.

Pre-requisites: Install CDK and Configure AWS
Credentials[[Ref](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)]

```commandline
cd cdk
cdk synth
cdk deploy
```

# Usage

After deployment, you can execute the State Machine via AWS console or via AWS CLI

State Machine Input Example:

```json
{
  "stream_name": "test-stream",
  "desired_shard_count": 3
}
```

AWS CLI execution examole

```commandline
aws stepfunctions start-execution \
--state-machine-arn arn:aws:states:us-east-1:123456789:stateMachine:KinesisScalingWorkflow \
--input "{\"stream_name\": \"test-stream\", \"desired_shard_count\": 1}"
```

## Removal
```commandline
cd cdk
cdk destroy
```
Manually remove any retained Lambda CloudWatch Log Groups