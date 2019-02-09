"""Hub for invoking sub-parsers for each domain of interest."""
from . import gutenberg as gb


def parse(gutenberg=False, all=False, **kwargs):
    """Invoke parsers."""
    if all or gutenberg:
        gb.parse(**kwargs)
