'''Script to interact with DALL-E API.'''
import boto3
import datetime
import json


def generate_image(event, context) -> None:
    '''Uses a placeholder string.

    Assumes that some JSON response is returned with 
    a link to where the image is hosted.
    )
    '''
    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    datestamp = datetime.date.today()
    feature_json_name = f'feature_{datestamp}.json'

    s3 = boto3.client('s3')
    response = s3.get_object(
        Bucket='glimpse-feature-store', Key=feature_json_name
    )
    features = response['Body'].read().decode('utf-8')

    # simulates gpt3.5 prompt results
    features['img_prompt'] = r'placeholder_prompt'

    # simulates dall-e return results
    features['img_url'] = r'placeholder_url'

    # score JSON file with model results
    s3.put_object(
        Bucket='glimpse-feature-store',
        Key=feature_json_name,
        Body=bytes(json.dumps(features).encode('UTF-8'))
    )
    print('generate_image invoked')

    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:ap-southeast-2:906384561362:glimpse-img-gen-sns'
    sns.publish(TopicArn=topic_arn, Message='handler_image_gen function')

    print('Msg published to glimpse-img-gen-sns')

    return None
