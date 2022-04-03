import json
import unittest

from .kinesis_target_shard_calculator_lambda import lambda_handler
from .kinesis_target_shard_calculator_lambda import calculate_target_shard_count


class TestKinesisTargetShardCalculator(unittest.TestCase):

    def test_scale_up_calculate_target_shard_count(self):
        current_shard_count = 3
        desired_shard_count = 5
        expected_target_shard_count = 5
        actual_target_shard_count = calculate_target_shard_count(current_shard_count, desired_shard_count)
        self.assertEqual(expected_target_shard_count, actual_target_shard_count)

    def test_scale_up_threshold_calculate_target_shard_count(self):
        current_shard_count = 3
        desired_shard_count = 20
        expected_target_shard_count = 6
        actual_target_shard_count = calculate_target_shard_count(current_shard_count, desired_shard_count)
        self.assertEqual(expected_target_shard_count, actual_target_shard_count)

    def test_scale_down_calculate_target_shard_count(self):
        current_shard_count = 10
        desired_shard_count = 6
        expected_target_shard_count = 6
        actual_target_shard_count = calculate_target_shard_count(current_shard_count, desired_shard_count)
        self.assertEqual(expected_target_shard_count, actual_target_shard_count)

    def test_scale_down_threshold_calculate_target_shard_count(self):
        current_shard_count = 10
        desired_shard_count = 3
        expected_target_shard_count = 5
        actual_target_shard_count = calculate_target_shard_count(current_shard_count, desired_shard_count)
        self.assertEqual(expected_target_shard_count, actual_target_shard_count)

    def test_lambda_handler(self):
        request_json_str = '''
        {
            "stream_name": "flame-thrower",
            "desired_shard_count": 8,
            "describe_stream_output": {
                "StreamDescriptionSummary": {
                    "OpenShardCount": 5
                }
            }
        } 
        '''
        request_event = json.loads(request_json_str)
        expected_response = {
            'stream_name': 'flame-thrower',
            'desired_shard_count': 8,
            'target_shard_count': 8
        }
        actual_target_shard_count = lambda_handler(request_event, None)
        self.assertEqual(expected_response, actual_target_shard_count)


if __name__ == '__main__':
    unittest.main()
