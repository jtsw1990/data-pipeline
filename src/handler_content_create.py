'''Function to create content automatically.'''

import smtplib
import ssl
import os


def create_content(event, context) -> None:
    '''Lambda function creates content.'''

    print('create_content function invoked')

    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(os.environ['email_add'], os.environ['email_pw'])
        server.sendmail(
            os.environ['email_add'], os.environ['email_add'], message)

    print('create_content function invoked')

    return None
