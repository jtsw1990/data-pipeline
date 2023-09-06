'''Main script to extract and load feed into S3.'''

import os
from dotenv import load_dotenv
from extract_feed import extract_news_feed
from ingest_feed import ingest_news_feed


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
