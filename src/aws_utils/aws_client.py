"""Minimal AWS client wrapper (S3/DynamoDB) used by the monitor.

This module provides tiny helper methods. In production you would set up
credentials, retries, and robust error handling.
"""
import os
from typing import Any


class AWSClient:
    def __init__(self):
        try:
            import boto3
            self.boto3 = boto3
            self.s3 = boto3.client("s3")
            self.ddb = boto3.resource("dynamodb")
        except Exception:
            self.boto3 = None
            self.s3 = None
            self.ddb = None

    def put_object(self, bucket: str, key: str, body: bytes) -> Any:
        if not self.s3:
            raise RuntimeError("boto3 not available or not configured")
        return self.s3.put_object(Bucket=bucket, Key=key, Body=body)

    def put_metric(self, name: str, value: float) -> None:
        # Placeholder: in a real setup you'd use CloudWatch put_metric_data
        # Here we simply print for demonstration or could write to DynamoDB
        print(f"METRIC {name}={value}")

    def write_item(self, table_name: str, item: dict) -> Any:
        if not self.ddb:
            raise RuntimeError("boto3 not available or not configured")
        table = self.ddb.Table(table_name)
        return table.put_item(Item=item)


def example():
    aw = AWSClient()
    try:
        aw.put_metric("demo.test", 1)
    except Exception as e:
        print("AWS not configured:", e)


if __name__ == "__main__":
    example()
