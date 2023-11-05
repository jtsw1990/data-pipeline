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
    selected_section = content_json['selected_section']
    img_prompt = content_json['img_prompt']
    img_byte_str = content_json['img_byte_str']

    # Decode the base64-encoded image data from the dictionary
    img_bytes = base64.b64decode(img_byte_str.encode('utf-8'))

    user_email = os.environ['email_add']
    password = os.environ['email_pw']

    msg = MIMEMultipart("alternative")
    msg["From"] = user_email
    msg["To"] = user_email
    msg["Subject"] = f'Glimpse Feed:{message}'

    text = f"""\
    Original Title: {title}
    {selected_section}
    {img_prompt}
    {img_url}
    """
    html = f"""\
    <html>
    <body>
        <p>Original Title: {title}<br>
        <p>Selected Section: {selected_section}<br>
        <p>Image Prompt: {img_prompt}<br>
        <a href={img_url}>Image</a>
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    image = MIMEImage(img_bytes, name=f"image_{message}.jpg")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)
    msg.attach(image)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(user_email, password)
        server.sendmail(
            user_email, user_email, msg.as_string()
        )
    print('create_content function invoked')

    return None

# %%
