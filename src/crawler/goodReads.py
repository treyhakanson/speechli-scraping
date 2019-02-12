"""GoodReads sub-crawler."""
import csv
from urllib.parse import urlparse
from .constants import DATA_DIR
from .crawlable import Crawlable


BASE_DIR = DATA_DIR.joinpath("goodreads")
BASE_URLS = (
    (
        "quotes/BarackObama/index.csv",
        "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=Barack+Obama&commit=Search"
    ),
    (
        "quotes/MahatmaGandhi/index.csv",
        "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=Mahatma+Gandhi+&commit=Search"
    ),
)


def setup():
    """Setup the directories for crawling Project GoodReads."""
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)

def write(fpath, data):
    """Write data to a csv."""
    with fpath.open(mode="w") as csvfile:        
        for element in data:
            csvfile.write(str(element).strip('\"') + "\n")


def retrieve_quotes()  :
    """Retrieve quotes."""
    setup()
    for loc, url in BASE_URLS:
        data = []
        fpath = BASE_DIR.joinpath(loc)
        if not fpath.parent.exists():
            fpath.parent.mkdir(parents=True)
        crawlable = Crawlable(url)
        crawlable.retrieve()
        tags = crawlable._soup.find_all(attrs={"class":"quoteText"})
        for tag in tags:
            array = tag.text.split("\n")
            for string in array: 
                if (len(string) > 5 and not tag.script): data.append(string)
        data = data[::2]
        write(fpath, data)
