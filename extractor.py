import abc
import urllib.request

class BaseNewsExtractor:
    def __init__(self, url):
        self.url = url

    def _load_page(self):
        page = urllib.request.urlopen(self.url)
        content = page.read()
        return content

    @abc.abstractmethod
    def get_name(self):
        return "BaseNews"

    @abc.abstractmethod
    def extract_articles(self, html_content):
        """Return a list of news headlines in the form of
        [[news_category, href, header, summary]]. If any of these elements
         do not exist, place an empty string"""
        return

    def get_daily_articles(self):
        content = self._load_page()
        articles = self.extract_articles(content)
        return articles
