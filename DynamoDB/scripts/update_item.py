from botocore.exceptions import ClientError
from db import dynamodb

TABLE_NAME = 'users'

def main():
    table  = dynamodb.Table(TABLE_NAME)

    try:
        resp = table.update_item(
            Key={"pk": "USER#1001","sk":"PROFILE"},
            UpdateExpression="SET #n = :name",
            ExpressionAttributeNames={"#n": "name"},
            ExpressionAttributeValues={":name": "Sanket Updated"},
            ReturnValues="ALL_NEW",     
        )
    except ClientError as e:
        print("Error", e)
        return

    print("Updated item:")
    print(resp.get("Attributes"))

if __name__ == "__main__":
    main()