"""Hub for invoking sub-crawlers for each domain of interest."""
from .gutenberg import retrieve_index as gb
from .genius import retrieve_index as gen


def crawl(gutenberg=False, genius=False, all=False):
    """Invoke crawlers."""
    if all:
        gb()
        gen()
    elif genius:
        gen()
    elif gutenberg:
        gb()
