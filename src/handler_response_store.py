import boto3


def store_response(event, context) -> None:
    '''Lambda function stores generated image into S3.'''

    print('store_response function invoked')

    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')
    print('store_response invoked')

    return None
