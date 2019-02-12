"""Hub for invoking sub-parsers for each domain of interest."""
from . import gutenberg as gb
from . import genius as gen


def parse(gutenberg=False, genius=False, all=False, **kwargs):
    """Invoke parsers."""
    if all or gutenberg:
        gb.parse(**kwargs)
    elif all or genius:
        gen.parse(**kwargs)
