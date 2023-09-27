'''Script to interact with DALL-E API.'''
import boto3
import datetime


def generate_image(event, context) -> None:
    '''Uses a placeholder string.

    Assumes that some JSON response is returned with 
    a link to where the image is hosted.
    )
    '''
    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    datestamp = datetime.date.today()

    s3 = boto3.client('s3')
    response = s3.get_object(
        Bucket='glimpse-feature-store', Key=f'feature_{datestamp}.json'
    )
    features = response['Body'].read().decode('utf-8')

    print(features)

    print('generate_image invoked')

    result = 'Image response'
    print('Image returned')
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:ap-southeast-2:906384561362:glimpse-img-gen-sns'
    sns.publish(TopicArn=topic_arn, Message='handler_image_gen function')

    print('Msg published to glimpse-img-gen-sns')

    return None
