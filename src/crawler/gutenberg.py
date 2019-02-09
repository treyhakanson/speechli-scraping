"""Gutenberg sub-crawler."""
import re
import csv
from urllib.parse import urlparse
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
    """Write data to a csv, or dump it in a text file."""
    if isinstance(data, list):
        with fpath.open(mode="w") as csvfile:
            csvwriter = csv.writer(
                csvfile,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )
            csvwriter.writerows(data)
    else:
        with fpath.open(mode="w") as f:
            f.write(data)


def get_plaintext_url(index_url):
    """Get the url of the plaintext based on the index link."""
    url = urlparse(index_url)
    match = re.search(r"/(\d+)$", url.path)
    key = match.group(1)
    plaintext_url = f"http://www.gutenberg.org/cache/epub/{key}/pg{key}.txt"
    return key, plaintext_url


def retrieve_index(no_cache=False):
    """Retrieve the gutenberg indexes."""
    setup()
    for loc, url in BASE_URLS:
        fpath = BASE_DIR.joinpath(loc)
        print(f"{url} -> {loc}...")
        if not no_cache and fpath.exists():
            # If we are using the cache and the result exists, skip
            print(f"\tUsing cached results.")
            continue
        if not fpath.parent.exists():
            fpath.parent.mkdir(parents=True)
        crawlable = Crawlable(url)
        crawlable.retrieve()
        data = [(clean(link),) for link in crawlable.parse("li > .extiw")]
        write(fpath, data)
        print(f"\tSuccessfully retrieved index.")


def retrieve_from_index(no_cache=False):
    """Retrieve the books from the index."""
    for loc, url in BASE_URLS:
        fpath = BASE_DIR.joinpath(loc)
        with fpath.open(mode="r") as csvfile:
            csvreader = csv.reader(
                csvfile,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )
            for row in csvreader:
                index_url = row[0]
                key, plaintext_url = get_plaintext_url(index_url)
                book_fpath = fpath.parent.joinpath(f"{key}.txt")
                print(
                    f"{plaintext_url} -> {book_fpath}"
                )
                if not no_cache and book_fpath.exists():
                    # If we are using the cache and the result exists, skip
                    print(f"\tUsing cached results.")
                    continue
                crawlable = Crawlable(plaintext_url)
                crawlable.retrieve()
                text = crawlable.dump()
                write(book_fpath, text)
                print(f"\tSuccessfully retrieved book.")


def fetch(**kwargs):
    """Fetch the indexes, and the retrieve the books from those indexes."""
    retrieve_index(**kwargs)
    retrieve_from_index(**kwargs)
