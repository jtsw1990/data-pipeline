'''Script to interact with DALL-E API.'''
# %%
import boto3
import json
import openai
import os
import requests
import base64
import time


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
    leonardo_api_key = os.environ['leonardo_api_key']

    prompt_template = '''
    Using the following snippet encased in ``, generate an image prompt of an imaginery human superhero or superheroine that is relevant to the snippet, be creating and detailed in the description of this character.
    Also come up with a creative backstory in around 50 words on this hero's origin story and his/her main superpower, and include some elements of the original snippet in the backstory.
    
    `Faces of hope: The freed hostages of Gaza`
    '''  # noqa: E501

    response_template = '''
    Imaginary Superhero: Lumina Salvator

    Description:
    Lumina Salvator, draped in a radiant cloak, emanates a warm glow reflecting the faces of the freed hostages. Their eyes shine with compassion, symbolizing the transformative power of hope emerging from the shadows.

    Backstory:
    Sarah Al-Hassan, a photojournalist, harnessed the energy of hope captured in her lens. Empowered, she became Lumina Salvator, using the light of captured moments to inspire healing and unity.

    Main Superpower:
    Photonic Healing - Lumina Salvator can harness and project healing energy through captured images, bringing solace and empowerment to those who have endured trauma, embodying the resilience of the freed hostages in Gaza.
    '''  # noqa: E501

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'system',
                'content': 'You are a creative character designer'
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
                'content': f'Do the same for the following snippet: `{initial_prompt}`'  # noqa: E501
            }
        ]
    )

    image_prompt = completion.choices[0].message.content

    features['img_prompt'] = image_prompt

    # Leonardo API

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        "height": 512,
        "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132",
        "prompt": image_prompt,
        "width": 512,
        "alchemy": True,
        "highResolution": True,
        "nsfw": True,
        "num_images": 1,
        "photoReal": False,
        "presetStyle": "CINEMATIC",
        "expandedDomain": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {leonardo_api_key}"
    }
    response = requests.post(url, json=payload, headers=headers)

    for k in range(25):
        print(f'Sleeping...{k}')
        time.sleep(1)

    gen_id = response.json()['sdGenerationJob']['generationId']

    get_gen_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{gen_id}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {leonardo_api_key}"
    }

    response = requests.get(get_gen_url, headers=headers)

    img_url = (
        response.json()
        ['generations_by_pk']
        ['generated_images'][0]['url']
    )

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
