'''Script to interact with DALL-E API.'''

import boto3
import json
import openai
import os


def generate_image(event, context) -> None:
    '''Uses a placeholder string.

    Assumes that some JSON response is returned with 
    a link to where the image is hosted.
    )
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

    # GPT prompt
    openai.api_key = os.environ['openai_key']

    prompt_template = '''
    Can you adjust the following sentence surrounded by ``` with the following:
    - Adjust the sentence into one describing a person or a scene in less than 25 words
    - Replace any names with a description of their age, gender and ethnicity
    - Replace any political agendas to something more ambiguous
    - Be as descriptive as possible about the subject so that DALL-E can comprehend
    - Add in "A street photo of" to the start of the response
    - Add in "shot by a Leica." at the back of the response
    ```Bangladesh's worst ever dengue outbreak a 'canary in the coal mine' for climate crisis, WHO expert warns```
    '''

    response_template = '''A street photo of a concerned middle-aged Asian woman, her brows furrowed, emphasizing climate impact, shot by a Leica.'''

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'system',
                'content': 'You are a expert writer and prompt expert'
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
                'content': 'Do the same for the sentence ```Naomi Osaka announces return to professional tennis in 2024```'
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

    features['img_url'] = img_url

    # score JSON file with model results
    s3.put_object(
        Bucket='glimpse-feature-store',
        Key=feature_json_name,
        Body=bytes(json.dumps(features).encode('UTF-8'))
    )
    print('generate_image invoked')

    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:ap-southeast-2:906384561362:glimpse-img-gen-sns'
    sns.publish(TopicArn=topic_arn, Message=message)

    print('Msg published to glimpse-img-gen-sns')

    return None
