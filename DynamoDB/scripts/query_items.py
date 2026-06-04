from botocore.exceptions import ClientError
from db import dynamodb
from boto3.dynamodb.conditions import Key

TABLE_NAME = 'users'


def main():

    table = dynamodb.Table(TABLE_NAME)

    try:
        response = table.query(
            KeyConditionExpression=Key('pk').eq('USER#1001')
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return 

    print("Count: ", response.get("Count"))
    for item in response.get("Items", []):
        print(item)


if __name__ == "__main__":
    main()