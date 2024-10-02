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
    if not articles:
        print(f"There is no article yet for {today}!")
    with open('output.txt', 'w') as f:
        for href, hdr, txt in articles:
            f.writelines([hdr, '\r\n'])
            f.writelines([href, '\r\n'])
            f.write(txt)
            f.write('\r\n')
            f.write('\r\n')




