from extractor import BaseNewsExtractor
from bs4 import BeautifulSoup as BS
from datetime import datetime
import re

class SourceTLDR(BaseNewsExtractor):
    def __init__(self):
        today = datetime.today()
        today = today.strftime("%Y-%m-%d")
        print(today)
        url = f"https://tldr.tech/ai/{today}"
        super().__init__(url=url)

    def extract_articles(self, html_content):
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
            cat = ""
            res.append([cat, href, header, body])

        return res
