"""Parser for content from GoodReads."""
import json
from .constants import DATA_DIR

BASE_DIR = DATA_DIR.joinpath("goodreads")


def iterate(fpath):
    """Iterate over arbitrarily nested directories."""
    if not fpath.is_dir():
        yield fpath
    else:
        for subpath in fpath.iterdir():
            yield from iterate(subpath)


def parse(no_cache=False, **kwargs):
    """Parse all content from GoodReads."""
