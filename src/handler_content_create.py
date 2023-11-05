'''Function to send content to email automatically.'''
# %%
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import boto3
import base64


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
    img_byte_str = content_json['img_byte_str']

    # Decode the base64-encoded image data from the dictionary
    img_bytes = base64.b64decode(img_byte_str.encode('utf-8'))

    user_email = os.environ['email_add']
    password = os.environ['email_pw']

    message = MIMEMultipart("alternative")
    message["From"] = user_email
    message["To"] = user_email
    message["Subject"] = f'Glimpse content feed: {message}'

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
    image = MIMEImage(img_bytes, name="generated_image.jpg")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    message.attach(image)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(user_email, password)
        server.sendmail(
            user_email, user_email, message.as_string()
        )
    print('create_content function invoked')

    return None

# %%
