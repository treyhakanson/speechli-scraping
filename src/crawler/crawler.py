"""Hub for invoking sub-crawlers for each domain of interest."""
from . import gutenberg as gb, genius as gen


def crawl(gutenberg=False, genius=False, all=False, **kwargs):
    """Invoke crawlers."""
    if all or genius:
        gen.retrieve_index()
    elif all or gutenberg:
        gb.fetch(**kwargs)
