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
    Using the following snippet encased in ```, generate an image prompt of a robot that is inspired by a mix of Transformers, Gundam and Samurai armour, and is relevant to the snippet. The robot must take the shape of a random animal. Be detailed in the description of this robot. Ensure that the design and mechanism of it's body is very intricate, using a suitable 3 colour palette that includes black as a base with accents of the other 2 colours.

    Also come up with a creative backstory in around 50 words on this robot's origin story, and include elements of the original snippet in the backstory.

    ```Sri Lanka Suffers Brief Power Outage After Main Transmission Line Fails```
    '''  # noqa: E501

    response_template = '''
    Design Description:
    Introducing "EnergiPanther," a robotic marvel blending Transformers, Gundam, and Samurai aesthetics. This sleek mechanized panther stands at 25 feet, adorned in intricate black armor with accents of deep crimson and electric gold. The samurai-inspired patterns on its chassis exude elegance, and its articulated limbs display a fusion of strength and precision.

    In a majestic pose, EnergiPanther prowls, its golden eyes gleaming with determination. The crimson energy pulsating through its tail signifies the power coursing through its cybernetic veins.

    Backstory:
    Forged by visionary Sri Lankan engineers post a crucial power outage, EnergiPanther embodies the nation's spirit. The main transmission line failure spurred its creation, fusing traditional samurai ethos with cutting-edge robotics. EnergiPanther now stands as a guardian, symbolizing Sri Lanka's commitment to overcoming challenges and ensuring an uninterrupted power supply.
    '''

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

    prompt = (
        image_prompt.replace('\n', '')
        .split('Design Description:')[-1]
        .split('Backstory:')[0]
    )
    final_text = image_prompt.replace('\n', '').split('Backstory:')[-1]

    features['img_prompt'] = final_text

    # Leonardo API

    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        "height": 512,
        "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132",
        "prompt": prompt,
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
