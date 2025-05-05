import feedparser
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
import re
from newspaper import Article
from curl_cffi.requests import AsyncSession
import asyncio
import pandas as pd
import logging
import sqlite3

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
        page = browser.new_page()
        redirected_links = []
        for link in rss_links:
            try: 
                page.goto(link)
                redirected_link = page.wait_for_url(pattern, timeout=10000)
                redirected_links.append(page.url)
            except TimeoutError:
                logging.warning(f'Timeout error for link: {link}')
            except Exception as e:
                logging.error(f'Error for link: {link}, Error: {e}')
        browser.close()
    return redirected_links

async def get_responses(links):
   async with AsyncSession() as session:
        tasks = []
        for link in links:
            tasks.append(session.get(link, impersonate='chrome'))
        responses = await asyncio.gather(*tasks)      
        valid_responses = [response for response in responses if response.status_code == 200] 
        return valid_responses

async def get_articles(links, category):
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
            'url': response.url,
            'category': category
        })
    return articles

def store_articles_in_db(articles):
    con = sqlite3.connect('articles_data.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS article")
    cur.execute("CREATE TABLE article(title, text, url, category)")

    for article in articles:
        cur.execute("INSERT INTO article VALUES (?, ?, ?, ?)", (article['title'], article['text'], article['url'], article['category']))
    con.commit()
    con.close()

if __name__ == '__main__':
    CATEGORY = 'Technology'
    feed_url = 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK:en'
    links = get_links_from_feed(feed_url)[:5]
    print(f'feed links: {links}')
    final_links = get_redirected_links(links)
    print(f'final links: {final_links}')
    articles = asyncio.run(get_articles(final_links, CATEGORY))
    print(f'articles: {articles}')
    store_articles_in_db(articles)

    


