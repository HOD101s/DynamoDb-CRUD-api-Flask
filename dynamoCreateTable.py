# Start Local DynamoDb
# java -Djava.library.path=./DynamoDBLocal_lib -jar "Path To DynamoDBLocal.jar" -sharedDb
import boto3

ddb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

dbtable = ddb.create_table(
    TableName='tasks',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'added_date',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'added_date',
            'AttributeType': 'N'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
