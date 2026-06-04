from botocore.exceptions import ClientError
from db import dynamodb

TABLE_NAME = "users"


def main():
    table = dynamodb.Table(TABLE_NAME)

    try:
        table.delete_item(
            Key={"pk": "USER#1001", "sk": "PROFILE"},
        )
        print("Deleted USER#1001")
    except ClientError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()