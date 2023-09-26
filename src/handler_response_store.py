import boto3
import datetime
import json


def store_response(event, context) -> None:
    '''Lambda function stores generated image into S3.'''

    print('store_response function invoked')

    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    s3 = boto3.resource('s3')
    bucket = s3.Object('glimpse-img-response-store',
                       f'content_{datetime.date.today()}.json')

    bucket.put(
        Body=(bytes(json.dumps(message).encode('UTF-8')))
    )

    print('store_response invoked')

    return None
