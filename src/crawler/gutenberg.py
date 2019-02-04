"""Gutenberg sub-crawler."""
import csv
from .constants import DATA_DIR
from .crawlable import Crawlable


BASE_DIR = DATA_DIR.joinpath("gutenberg")
BASE_URLS = (
    (
        "bookshelf/adventure/index.csv",
        "https://www.gutenberg.org/wiki/Adventure_(Bookshelf)"
    ),
    (
        "bookshelf/science-fiction/index.csv",
        "https://www.gutenberg.org/wiki/Science_Fiction_(Bookshelf)"
    ),
    (
        "bookshelf/fantasy/index.csv",
        "https://www.gutenberg.org/wiki/Fantasy_(Bookshelf)"
    ),
)


def setup():
    """Setup the directories for crawling Project Gutenberg."""
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)


def clean(link):
    """Clean links."""
    return "http:" + link.get("href")


def write(fpath, data):
    """Write data to a csv."""
    with fpath.open(mode="w") as csvfile:
        csvwriter = csv.writer(
            csvfile,
            delimiter=',',
            quoting=csv.QUOTE_MINIMAL
        )
        csvwriter.writerows(data)


def retrieve_index():
    """Retrieve the gutenberg indexes."""
    setup()
    for loc, url in BASE_URLS:
        fpath = BASE_DIR.joinpath(loc)
        if not fpath.parent.exists():
            fpath.parent.mkdir(parents=True)
        crawlable = Crawlable(url)
        crawlable.retrieve()
        data = [(clean(link),) for link in crawlable.parse("li > .extiw")]
        write(fpath, data)
