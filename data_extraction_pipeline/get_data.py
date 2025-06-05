import feedparser
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
import re
from newspaper import Article
from curl_cffi.requests import AsyncSession
import asyncio
import logging
import pandas as pd
import os

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
    
def get_redirected_links(rss_links):
    rss_prefix = r'https://news\.google\.com/rss/articles/'
    pattern = re.compile(rf'^(?!{rss_prefix}).+')

    with sync_playwright() as playwright:
        chromium = playwright.chromium 
        browser = chromium.launch(headless=True)
        
        redirected_links = []
        for link in rss_links:
            try: 
                page = browser.new_page()
                page.goto(link)
                page.wait_for_url(pattern, timeout=10000)
                redirected_links.append(page.url)
            except TimeoutError:
                logging.warning(f'Timeout error for link: {link}')
            except Exception as e:
                logging.error(f'Error for link: {link}, Error: {e}')
            page.close()
        browser.close()
    return redirected_links

async def get_responses(links):
   async with AsyncSession() as session:
        tasks = []
        for link in links:
            tasks.append(session.get(link, impersonate='chrome', verify=False))
        responses = await asyncio.gather(*tasks)      
        valid_responses = [response for response in responses if response.status_code == 200] 
        return valid_responses

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
    """Save the articles csv file to the data directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_file_path = os.path.join(data_dir, 'articles.csv')
    with open(csv_file_path, 'w', encoding='utf-8') as f:
        data_final.to_csv(f, index=False)

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
        redirected_links = get_redirected_links(links)
        print(f'redirected links: {redirected_links}')
        articles = asyncio.run(get_articles(redirected_links))
        df = pd.DataFrame(articles)
        df['category'] = category
        data.append(df)
    data_final = pd.concat(data, ignore_index=True)
    data_final['text'] = data_final['text'].apply(lambda x: x.strip())
    data_final.dropna(subset=['text'], inplace=True)
    save_articles_to_csv(data_final)




