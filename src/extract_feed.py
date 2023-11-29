''''Loads raw JSON from Currents API.'''

# %%
from dotenv import load_dotenv
from currentsapi import CurrentsAPI
import os


def extract_news_feed(api_key: str) -> dict:
    '''Load JSON response containing latest news feed from Currents API.
    https://pypi.org/project/currentsapi/
    '''

    api = CurrentsAPI(api_key=api_key)

    return api.search(
        country="",
        language="en",
        category="world"
    )


if __name__ == '__main__':
    load_dotenv()
    currents_api_key = os.environ['currents_api_key']
    feed = extract_news_feed(currents_api_key)

# %%
