'''Ingest extracted feed into S3 bucket.'''

# %%
import boto3
import os
import json
import datetime
from dotenv import load_dotenv
from extract_feed import extract_news_feed


def ingest_news_feed(
    aws_access_key: str,
    aws_secret_key: str,
    aws_region: str,
    json_feed: dict
) -> None:
    '''Ingest currents API feed into specified S3 Bucket.'''

    s3 = boto3.resource(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)

    bucket = s3.Object(
        'glimpse-landing-dev',
        f'currents_raw_{datetime.date.today()}.json'
    )

    bucket.put(
        Body=(bytes(json.dumps(json_feed).encode('UTF-8')))
    )


if __name__ == '__main__':
    load_dotenv()
    aws_access_key = os.environ['aws_access_key']
    aws_secret_key = os.environ['aws_secret_key']
    aws_region = os.environ['aws_region']
    currents_api_key = os.environ['currents_api_key']
    news_feed_respons_json = extract_news_feed(currents_api_key)
    ingest_news_feed(
        aws_access_key,
        aws_secret_key,
        aws_region,
        news_feed_respons_json
    )
