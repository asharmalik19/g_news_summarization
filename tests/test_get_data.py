import sys
import os
import asyncio

import pytest
import pandas as pd

from g_news_summarization import (
    get_data,
    downloader
)

def test_clean_the_data():
    df = pd.DataFrame({
        'text': ['Good article', 'Try unlimited access to read more', ''],
        'title': ['Title 1', 'Title 2', 'Title 3']
    })
    cleaned_df = get_data.clean_the_data(df)
    assert cleaned_df.shape[0] == 1
    assert cleaned_df.iloc[0]['text'] == 'Good article'

def test_downloader():
    project_root = downloader.find_project_root()
    assert 'g-news-summarization' in project_root