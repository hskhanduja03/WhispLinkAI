import trafilatura
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_text_and_images(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    
    if not text:
        text = ""
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    images = []

    for img in soup.find_all('img'):
        src = img.get('src')
        alt = img.get('alt', '')
        if src:
            full_url = urljoin(url, src)
            images.append({'url': full_url, 'alt': alt})

    return text, images
