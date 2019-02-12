"""Hub for invoking sub-crawlers for each domain of interest."""
from . import gutenberg as gb, genius as gen, goodReads as gr


def crawl(gutenberg=False, genius=False, quotes=False, all=False, **kwargs):
    """Invoke crawlers."""
    if all or genius:
        gen.fetch(**kwargs)
    elif all or gutenberg:
        gb.fetch(**kwargs)
    elif all or quotes:
        gr.retrieve_quotes()      