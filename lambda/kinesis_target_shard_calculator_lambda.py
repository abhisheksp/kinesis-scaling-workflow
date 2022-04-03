def calculate_target_shard_count(current_shard_count, desired_shard_count):
    # scale up case
    if current_shard_count < desired_shard_count:
        return min(desired_shard_count, current_shard_count * 2)
    # scale down case
    return max(desired_shard_count, current_shard_count // 2)


def lambda_handler(event, context):
    # From Update Shard Count Request
    current_shard_count = event['describe_stream_output']['StreamDescriptionSummary']['OpenShardCount']
    desired_shard_count = event['desired_shard_count']
    target_shard_count = calculate_target_shard_count(current_shard_count, desired_shard_count)
    stream_name = event['stream_name']
    return {
        'stream_name': stream_name,
        'desired_shard_count': desired_shard_count,
        'target_shard_count': target_shard_count
    }
