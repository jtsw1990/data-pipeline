'''Function to send content to email automatically.'''
# %%
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import boto3


def create_content(event, context) -> None:
    '''Lambda function creates content.'''

    print('create_content function invoked')

    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    s3 = boto3.client('s3')

    feature_json_name = f'feature_{message}.json'

    response = s3.get_object(
        Bucket='glimpse-feature-store',
        Key=feature_json_name
    )
    content = response['Body'].read().decode('utf-8')
    content_json = eval(content)

    img_url = content_json['img_url']
    title = content_json['title']
    subject = f'Glimpse content feed: {message}'

    sender_email = os.environ['email_add']
    receiver_email = os.environ['email_add']
    password = os.environ['email_pw']

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Post: {title}
    {img_url}"""
    html = f"""\
    <html>
    <body>
        <p>Post: {title}<br>
        <a href={img_url}>Image</a>
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    print('create_content function invoked')

    return None

# %%
