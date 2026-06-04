# src/db.py

import os
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

from .exceptions import PersistenceError

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
USERS_TABLE = os.getenv("USERS_TABLE", "users")


_dynamodb_resource = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def _users_table():
    return _dynamodb_resource.Table(USERS_TABLE)


def put_user_item(item: Dict[str, Any]) -> None:
    """
    Persist a user item in DynamoDB.
    """
    table = _users_table()
    try:
        table.put_item(Item=item)
    except ClientError as e:
        raise PersistenceError(str(e)) from e