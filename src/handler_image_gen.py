'''Script to interact with DALL-E API.'''
# %%
import boto3
import json
import openai
import os
import requests
import base64


def generate_image(event, context) -> None:
    '''Score feature JSON object with 3 properties.

    - img_prompt
    - img_url
    - img_data
    '''
    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')

    feature_json_name = f'feature_{message}.json'

    s3 = boto3.client('s3')
    response = s3.get_object(
        Bucket='glimpse-feature-store', Key=feature_json_name
    )
    features = response['Body'].read().decode('utf-8')
    features = eval(features)

    initial_prompt = features['selected_section']

    # GPT prompt
    openai.api_key = os.environ['openai_key']

    prompt_template = '''
    Use the one main object or topic in the following news snippet and generate a creative DALL-E prompt using a 3d style in less than 30 words:
    Bangladesh's worst ever dengue outbreak a 'canary in the coal mine' for climate crisis, WHO expert warns
    '''  # noqa: E501

    response_template = '''Produce a 3D artwork featuring the 'canary in the coal mine' symbolism for the climate crisis, with a spotlight on the dengue outbreak's significance.'''  # noqa: E501

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'system',
                'content': 'You are a professional graphic designer'
            },
            {
                'role': 'user',
                'content': prompt_template
            },
            {
                'role': 'assistant',
                'content': response_template
            },
            {
                'role': 'user',
                'content': f'Generate another DALL-E prompt for the following snippet: ```{initial_prompt}```'  # noqa: E501
            }
        ]
    )

    image_prompt = completion.choices[0].message.content

    features['img_prompt'] = image_prompt

    # DALL-E Prompt
    response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="512x512",
    )

    img_url = response["data"][0]["url"]
    img_bytes = requests.get(img_url).content

    img_byte_str = base64.b64encode(img_bytes).decode('utf-8')

    features['img_url'] = img_url
    features['img_byte_str'] = img_byte_str

    # score JSON file with model results
    s3.put_object(
        Bucket='glimpse-feature-store',
        Key=feature_json_name,
        Body=json.dumps(features)
    )
    print('generate_image invoked')

    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:ap-southeast-2:906384561362:glimpse-img-gen-sns'
    sns.publish(TopicArn=topic_arn, Message=message)

    print('Msg published to glimpse-img-gen-sns')

    return None

# %%
