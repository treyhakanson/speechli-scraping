"""Hub for invoking sub-crawlers for each domain of interest."""
from .gutenberg import fetch as gb
from .genius import retrieve_index as gen


def crawl(gutenberg=False, genius=False, all=False, **kwargs):
    """Invoke crawlers."""
    if all or genius:
        gen()
    elif all or gutenberg:
        gb(**kwargs)
