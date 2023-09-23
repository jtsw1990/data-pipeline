'''Processes news titles into usable image prompt.'''
# %%
from pandas import DataFrame


def process_table_into_prompt(df: DataFrame) -> str:
    '''Processes strings into a usable prompt.

    Read in processed dataframe (from local?).
    Remove any stop words?
    Extract single string ready to be fed into LLM.
    '''

    selected_string = '. '.join(df['selected_section'])

    return selected_string
