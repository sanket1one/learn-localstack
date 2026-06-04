from botocore.exceptions import ClientError
from datetime import datetime
from db import dynamodb


TABLE_NAME = "users"


def main():
    table = dynamodb.Table(TABLE_NAME)
    item = {
        "pk": "USER#1001",
        "sk": "PROFILE",
        "user_id": "1001",
        "username": "sanket",
        "email": "sanket@example.com",
        "role":"developer",
        "created_at": datetime.now().isoformat(),
    }

    try:
        table.put_item(Item=item)
        print("Item inserted successfully")
    except ClientError as e:
        print(e.response['Error']['Message'])



if __name__ == "__main__":
    main()