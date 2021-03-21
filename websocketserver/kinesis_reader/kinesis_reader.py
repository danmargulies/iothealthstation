import boto3

# import json
# from datetime import datetime
import time


class CKinesisReader:
    def __init__(self, streamName, region):
        self.my_stream_name = streamName
        self.read_limit = 1
        self.iterator_type = "LATEST"
        self.kinesis_client = boto3.client("kinesis", region_name=region)

        response = self.kinesis_client.describe_stream(StreamName=self.my_stream_name)

        self.my_shard_id = response["StreamDescription"]["Shards"][0]["ShardId"]

    def startPolling(self, fn):
        shard_iterator = self.kinesis_client.get_shard_iterator(
            StreamName=self.my_stream_name, ShardId=self.my_shard_id, ShardIteratorType=self.iterator_type
        )
        my_shard_iterator = shard_iterator["ShardIterator"]
        record_response = self.kinesis_client.get_records(ShardIterator=my_shard_iterator, Limit=self.read_limit)
        while "NextShardIterator" in record_response:
            record_response = self.kinesis_client.get_records(
                ShardIterator=record_response["NextShardIterator"], Limit=self.read_limit
            )
            for i in record_response["Records"]:
                print(i["Data"])
                fn(i["Data"])
            # wait for 5 seconds
            time.sleep(1)
