from datetime import datetime as dt

import pandas as pd
import json
import urllib.parse
import boto3


def process_data(event, context) -> None:
    '''Lambda function reads in latest JSON data and processes fields.'''

    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)

        result = pd.DataFrame(json_content['news'])
        result = result.replace(r'\n', '', regex=True).replace(
            r'\t', '', regex=True)
        result['category'] = result['category'].apply(lambda x: ', '.join(x))
        # Exract time & date features
        date_format = '%Y-%m-%d %H:%M:%S %z'
        result['publish_ts'] = result['published'].apply(
            lambda x: dt.strptime(x, date_format))
        result['publish_date'] = result['publish_ts'].apply(lambda x: x.date())
        result['publish_time'] = result['publish_ts'].apply(lambda x: x.time())

        # Clean and extract features from title
        result['title_token_count_raw'] = result['title'].apply(
            lambda x: len(x.split(' ')))
        result['split'] = result['title'].apply(
            lambda x: x.replace('--', ':').replace('|', ':').split(':'))
        result['split_length'] = result['split'].apply(
            lambda x: [len(p.split(' ')) for p in x])
        result['longest_section_len'] = result['split_length'].apply(
            lambda x: max(x))
        result['longest_section_idx'] = result.apply(
            lambda x: x['split_length'].index(x['longest_section_len']), axis=1)
        result['selected_section'] = result.apply(
            lambda x: x['split'][x['longest_section_idx']].strip(), axis=1)
        result['title_token_count_adj'] = result['selected_section'].apply(
            lambda x: len(x.split(' ')))

        print('process_data function invoked!')

        sns = boto3.client('sns')
        topic_arn = 'arn:aws:sns:ap-southeast-2:906384561362:glimpse-process-data-sns'

        message = {'content': result['selected_section'][0]}

        sns.publish(TopicArn=topic_arn, Message=message)

        print('Msg published to glimpse-process-data-sns')

        return None

    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}.'.format(key, bucket))
        raise e
