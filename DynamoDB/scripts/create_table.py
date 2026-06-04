from botocore.exceptions import ClientError
from db import dynamodb

TABLE_NAME = 'users'


def main():
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {'AttributeName': 'pk','KeyType': 'HASH'},
            {'AttributeName': 'sk', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'pk','AttributeType': 'S'},
            {'AttributeName': 'sk','AttributeType': 'S'},
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    print("Creating table, waiting until exists...")
    table.wait_until_exists()
    print("Table status:", table.table_status)



if __name__ == "__main__":
    try:
        main()
    except ClientError as e:
        print(e.response['Error']['Message'])
    