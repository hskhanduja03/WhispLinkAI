import asyncio
import sys
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def scrape_text_and_images(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')

    texts = []
    for tag in soup.find_all(['p', 'li', 'h1', 'h2', 'h3']):
        if tag.get_text(strip=True):
            texts.append(tag.get_text(strip=True))

    full_text = "\n".join(texts)

    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        alt = img.get('alt', '')
        if src:
            full_url = urljoin(url, src)
            images.append({'url': full_url, 'alt': alt})

    return full_text, images
