"""Utility class to help with retrieval of data."""
import requests
from bs4 import BeautifulSoup


class Crawlable:
    """Class defining a crawlable object."""

    def __init__(self, base_url):
        """Constructor."""
        self._base_url = base_url
        self.available = False

    def retrieve(self):
        """Retrieve the crawlable."""
        html = requests.get(self._base_url).content
        self._soup = BeautifulSoup(html, features="html.parser")
        self.available = True

    def parse(self, selector):
        """Run a selector against the retrieved data."""
        assert self.available, "Cannot parse crawlable before retrieval"
        data = self._soup.select(selector)
        return data
