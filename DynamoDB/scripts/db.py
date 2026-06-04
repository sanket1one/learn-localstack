import os
import boto3
from boto3.resources.base import ServiceResource

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")


def get_dynamodb() -> ServiceResource:
    return boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        endpoint_url=AWS_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

dynamodb = get_dynamodb()