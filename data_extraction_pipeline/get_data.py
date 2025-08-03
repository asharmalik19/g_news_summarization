import os
import re
import numpy as np
import asyncio
import logging

import feedparser
from newspaper import Article
from curl_cffi.requests import AsyncSession
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError

logging.basicConfig(
    level=logging.INFO,
    filename='data_extraction.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def get_links_from_feed(url):
    d = feedparser.parse(url)
    links = []
    for entry in d.entries:
        links.append(entry.link)
    return links

async def render_link(link, browser, pattern, sem):  
    redirected_link = None
    async with sem:
        page = await browser.new_page()
        try:
            await page.goto(link)
            await page.wait_for_url(pattern, timeout=15000)
            redirected_link = page.url
        except TimeoutError:
            logging.warning(f'Timeout error for link: {link}')
        except Exception as e:
            logging.error(f'Error for link: {link}, Error: {e}')
        await page.close()
    return redirected_link

async def get_redirected_links(rss_links):
    rss_prefix = r'https://news\.google\.com/rss/articles/'
    pattern = re.compile(rf'^(?!{rss_prefix}).+')
    sem = asyncio.Semaphore(15)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        tasks = [render_link(link, browser, pattern, sem) for link in rss_links]
        redirected_links = await asyncio.gather(*tasks)
        await browser.close()
    redirected_links = [link for link in redirected_links if link is not None]
    return redirected_links

async def get_responses(links):
   async with AsyncSession() as session:
        tasks = []
        for link in links:
            tasks.append(session.get(link, impersonate='chrome', verify=False))
        responses = []
        results = await asyncio.gather(*tasks, return_exceptions=True)      
        for result in results:
            if isinstance(result, Exception):
                logging.warning(f'Request failed by curl-cffi: {result}')
                continue
            if result.status_code == 200:
                responses.append(result)
        return responses

async def get_articles(links):
    responses = await get_responses(links)
    articles = []
    for response in responses:
        html = response.text
        article = Article(response.url)
        article.set_html(html)
        article.parse()
        articles.append({
            'title': article.title,
            'text': article.text,
            'url': response.url
        })
    return articles

def save_articles_to_csv(data_final):
    """Save the articles csv file to the data directory at project root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_file_path = os.path.join(data_dir, 'articles.csv')
    with open(csv_file_path, 'w', encoding='utf-8') as f:
        data_final.to_csv(f, index=False)

def clean_the_data(df):
    """The newspaper library can sometimes return articles with empty text
    and there are also articles behind paywalls that needs to be cleaned.
    """
    df['text'] = df['text'].apply(lambda x: np.nan if 'Try unlimited access' in x else x)
    df['text'] = df['text'].replace('', np.nan)
    df.dropna(subset=['text'], inplace=True)
    df['text'] = df['text'].apply(lambda x: x.strip())
    return df
    

if __name__ == '__main__':
    categories_and_feed_urls = {
        'Technology': 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK:en',
        'Business': 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK:en',
        'World': 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK:en'
    }
    data = []
    for category, feed_url in categories_and_feed_urls.items():
        links = get_links_from_feed(feed_url)
        print(f'feed links: {links}')
        redirected_links = asyncio.run(get_redirected_links(links))
        print(f'redirected links: {redirected_links}')
        articles = asyncio.run(get_articles(redirected_links))
        df = pd.DataFrame(articles)
        df['category'] = category
        data.append(df)
    data_final = pd.concat(data, ignore_index=True)
    cleaned_data_final = clean_the_data(data_final)
    save_articles_to_csv(cleaned_data_final)




