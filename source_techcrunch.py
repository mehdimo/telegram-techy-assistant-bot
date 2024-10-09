from extractor import BaseNewsExtractor
from bs4 import BeautifulSoup as BS

class SourceTechCrunch(BaseNewsExtractor):
    def __init__(self):
        url = "https://techcrunch.com/category/artificial-intelligence/"
        super().__init__(url=url)

    def extract_articles(self, html_content):
        soup = BS(html_content, features="html.parser")
        elements = soup.find_all('div', {"class": "loop-card__content"})
        res = []
        for e in elements:
            category = e.find('div', {"class": "loop-card__cat-group"})
            if category:
                category = category.text.strip()
                if "TechCrunch" in category:
                    continue
                time_ = e.find('time')
                ts = time_.text.strip()
                if ts == '1 day ago' or 'hour' in ts:
                    body = e.find('h3')
                    header = body.text.strip()
                    link = body.find('a')
                    href = link['href']
                    res.append([category, href, header, ""])
        return res
