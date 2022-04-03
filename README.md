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