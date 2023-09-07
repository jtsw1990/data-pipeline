'''Read and process data from S3.'''
# %%
import boto3
import json
import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from pandas import DataFrame


def load_data(
        aws_access_key: str,
        aws_secret_key: str,
        aws_region: str
) -> dict:
    '''Loads the day's latest news into script.'''

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)

    bucket_name = 'glimpse-landing-dev'
    file_key = f'currents_raw_{datetime.date.today()}.json'

    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    file_content = response['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)

    return json_content


def process_data(response: dict) -> DataFrame:
    '''Transforms data into table for loading into warehouse.'''

    if response['status'] != 'ok':
        return 'Data not found!'
    result = pd.DataFrame(response['news'])
    result = result.replace(r'\n', '', regex=True)
    result['category'] = result.category.apply(lambda x: ', '.join(x))

    date_format = "%Y-%m-%d %H:%M:%S %z"
    result['publish_ts'] = result['published'].apply(
        lambda x: datetime.datetime.strptime(x, date_format))
    result['publish_date'] = result['publish_ts'].apply(lambda x: x.date())
    result['publish_time'] = result['publish_ts'].apply(lambda x: x.time())

    return result


if __name__ == '__main__':
    load_dotenv()
    aws_access_key = os.environ['aws_access_key']
    aws_secret_key = os.environ['aws_secret_key']
    aws_region = os.environ['aws_region']

    response = load_data(aws_access_key, aws_secret_key, aws_region)
    result = process_data(response)
