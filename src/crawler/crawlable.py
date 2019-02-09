"""Utility class to help with retrieval of data."""
import requests
from bs4 import BeautifulSoup


class Crawlable:
    """Class defining a crawlable object."""

    def __init__(self, base_url):
        """Constructor."""
        self._base_url = base_url
        self.available = False
        self.success = False

    def retrieve(self):
        """Retrieve the crawlable."""
        res = requests.get(self._base_url)
        html = res.content
        self._soup = BeautifulSoup(html, features="html.parser")
        self.available = True
        self.success = res.ok

    def dump(self):
        """Dump the response data."""
        assert self.available, "Cannot parse crawlable before retrieval"
        data = self._soup.get_text()
        return data

    def parse(self, selector):
        """Run a selector against the retrieved data."""
        assert self.available, "Cannot parse crawlable before retrieval"
        data = self._soup.select(selector)
        return data
