'''Function to send content to email automatically.'''

import smtplib
import ssl
import os
import boto3
import datetime


def create_content(event, context) -> None:
    '''Lambda function creates content.'''

    print('create_content function invoked')

    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    s3 = boto3.client('s3')

    feature_json_name = f'feature_{message}.json'

    response = s3.get_object(
        Bucket='glimpse-feature-store', Key=feature_json_name
    )
    content = response['Body'].read().decode('utf-8')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(os.environ['email_add'], os.environ['email_pw'])
        server.sendmail(
            os.environ['email_add'], os.environ['email_add'], content)

    print('create_content function invoked')

    return None
