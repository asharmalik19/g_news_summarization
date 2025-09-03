import sys
import os
import asyncio

import pytest
import pandas as pd

# # Add the project root to Python path
# sys.path.insert(0,
# os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from g_news_summarization.get_data import clean_the_data

def test_clean_the_data():
    df = pd.DataFrame({
        'text': ['Good article', 'Try unlimited access to read more', ''],
        'title': ['Title 1', 'Title 2', 'Title 3']
    })
    cleaned_df = clean_the_data(df)
    assert cleaned_df.shape[0] == 1
    assert cleaned_df.iloc[0]['text'] == 'Good article'

