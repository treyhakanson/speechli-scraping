"""Hub for invoking sub-crawlers for each domain of interest."""
from .gutenberg import retrieve_index


def crawl(gutenberg=False, all=False):
    """Invoke crawlers."""
    if all or gutenberg:
        retrieve_index()
