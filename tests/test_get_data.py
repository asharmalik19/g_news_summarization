import sys
import os
import asyncio

import pytest

from data_extraction_pipeline.get_data import get_articles

async def test_get_articles():
    links = [
        'https://www.ft.com/content/ad5a6df0-da1d-4246-80c2-387d5cc7c541'
    ]
    articles = await get_articles(links)
    article = articles[0]
    # assert article['t
    print(article)

