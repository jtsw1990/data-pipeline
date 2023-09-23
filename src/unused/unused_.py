'''Read and process data from S3.'''
# %%
import boto3
import json
import os
import datetime
import pandas as pd
from datetime import datetime as dt
from dotenv import load_dotenv
from pandas import DataFrame


def get_json_from_s3(
        aws_access_key: str,
        aws_secret_key: str,
        aws_region: str,
        date_of_extract: dt = datetime.date.today()
) -> dict:
    '''Loads the day's latest news into script.'''

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)

    bucket_name = 'glimpse-landing-dev'
    file_key = f'currents_raw_{date_of_extract}.json'

    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    file_content = response['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)

    return json_content


def transform_json_to_df(response: dict) -> DataFrame:
    '''Transforms data into table for loading into warehouse.

    Returns
    '''

    if response['status'] != 'ok':
        return 'Data not found!'
    result = pd.DataFrame(response['news'])

    # Clean categories
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

    return result


if __name__ == '__main__':
    load_dotenv()
    aws_access_key = os.environ['aws_access_key']
    aws_secret_key = os.environ['aws_secret_key']
    aws_region = os.environ['aws_region']

    response = get_json_from_s3(
        aws_access_key, aws_secret_key, aws_region, date_of_extract='2023-09-07')
    result = transform_json_to_df(response)

# %%
