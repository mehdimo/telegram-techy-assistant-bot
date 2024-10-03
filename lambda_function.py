import json

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELE_BOT_TOKEN")
chatId = os.getenv("CHANNEL_CHAT_ID")
send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

import urllib.request
from bs4 import BeautifulSoup as BS
import re
from datetime import datetime

def extract_articles(html_content):
    soup = BS(html_content, features="html.parser")
    elements = soup.find_all('article')
    res = []
    for article in elements:
        link = article.find('a')
        href = link['href']
        href = href.replace("?utm_source=tldrai", "")

        # Get the header
        header = article.find('h3')
        header = header.text
        if "(Sponsor)" in header:
            continue
        header = re.sub(r'\(\d+ minute read\)', '', header)

        body = article.find('div')
        body = body.text
        res.append((href, header, body))

    return res

def load_page(url):
    page = urllib.request.urlopen(url)
    content = page.read()
    return content

def get_daily_articles():
    today = datetime.today()
    today = today.strftime("%Y-%m-%d")
    print(today)

    url = f"https://tldr.tech/ai/{today}"

    content = load_page(url)
    articles = extract_articles(content)
    return articles

def send_post():
    articles = get_daily_articles()
    for href, hdr, txt in articles:
        payload = f"<b>{hdr}</b>&#10&#10{txt}&#10&#10<a>{href}</a>&#10&#10 👉 https://t.me/aimleng" # newline: &#10
        requests.post(send_url, json={'chat_id': chatId, 'parse_mode': 'HTML',
                                      'text': payload})
    return len(articles)


def lambda_handler(event, context):
    cnt = send_post()
    print(f'Finished! {cnt} articles sent.')
    return {
        'statusCode': 200,
        'body': json.dumps(f'Done! {cnt} articles.')
    }
