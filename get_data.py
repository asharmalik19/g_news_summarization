import feedparser
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
import re
from newspaper import Article
from curl_cffi.requests import AsyncSession

def get_links_from_feed(url):
    d = feedparser.parse(url)
    links = []
    for entry in d.entries:
        links.append(entry.link)
    return links
    
def get_redirected_links(links):
    rss_prefix = r'https://news\.google\.com/rss/articles/'
    pattern = re.compile(rf'^(?!{rss_prefix}).+')

    with sync_playwright() as playwright:
        chromium = playwright.chromium 
        browser = chromium.launch(headless=True)
        page = browser.new_page()
        redirected_links = []
        for link in links:
            page.goto(link)
            try: 
                redirected_link = page.wait_for_url(pattern, timeout=10000)
                redirected_links.append(page.url)
            except TimeoutError:
                print(f'TimeoutError: {link}')
        browser.close()
    return redirected_links

async def gather_responses(links):
   async with AsyncSession() as session:
        tasks = []
        for link in links:
            tasks.append(session.get(link, impersonate='chrome'))
        responses = await asyncio.gather(*tasks)
        link_response_pairs = [(link, response) for link, response in zip(links, responses) if response.status_code == 200]
        return link_response_pairs

async def get_articles(links):
    link_response_pairs = await gather_responses(links)
    articles = []
    for link, response in link_response_pairs:
        html = response.text
        article = Article(link)
        article.set_html(html)
        article.parse()
        articles.append(article.text)
    return articles

if __name__ == '__main__':
    feed_url = 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK:en'
    links = get_links_from_feed(feed_url)[:10]
    print(f'feed links: {links}')
    final_links = get_redirected_links(links)
    print(f'final links: {final_links}')
    articles = await get_articles(final_links)
    for article in articles:
        print(article)
        print('---'*20)


    
