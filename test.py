import feedparser
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

def get_links_from_feed(url):
    d = feedparser.parse(url)
    links = []
    for entry in d.entries:
        links.append(entry.link)
    return links

def handle_cookies(page):
    try:
        cookies_btn = page.wait_for_selector('button:has-text("I Do Not Accept")', timeout=20000)
        cookies_btn.click()
    except TimeoutError:
        print('No cookies button found') 
    

def get_redirected_links(links):
    with sync_playwright() as playwright:
        chromium = playwright.chromium 
        browser = chromium.launch(headless=False)
        page = browser.new_page()
        redirected_links = []
        for link in links:
            page.goto(link)

            try:
                header = page.wait_for_selector('header', timeout=4000)
                header.click()
            except TimeoutError:
                print('No header found')
                     
            redirected_links.append(page.url)
            print(f'final url: {page.url}')
        browser.close()
    return redirected_links

if __name__ == '__main__':
    feed_url = 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK:en'
    links = get_links_from_feed(feed_url)
    final_links = get_redirected_links(links[:10])
    print(final_links)

    
