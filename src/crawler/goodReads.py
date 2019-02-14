"""GoodReads sub-crawler."""
import csv
import json
from .constants import DATA_DIR
from .crawlable import Crawlable


BASE_DIR = DATA_DIR.joinpath("goodreads")

BASE_URLS = [["quotes/BarackObama.json", "60", "https://www.goodreads.com/quotes/search?commit=Search&page=1&q=Barack+Obama&utf8=%E2%9C%93"],
            ["quotes/MahatmaGandhi.json", "40", "https://www.goodreads.com/quotes/search?commit=Search&page=1&q=Mahatma+Gandhi+&utf8=%E2%9C%93"],
            ["quotes/MartinLutherKingJr.json", "60", "https://www.goodreads.com/quotes/search?commit=Search&page=1&q=Martin+Luther+King+Jr&utf8=%E2%9C%93"]]

def setupLinks():
    """Setup links for crawling Project GoodReads."""
    for item in BASE_URLS:
        for i in range(2, int(item[1])):
            link = item[2]
            item.append(link.replace('1', str(i)))


def setup():
    """Setup the directories for crawling Project GoodReads."""
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)

def write(fpath, data):
    """Write data to a csv."""
    with fpath.open(mode="w") as f:
        json.dump(data, f)


def retrieve_quotes()  :
    """Retrieve quotes."""
    setup()
    setupLinks()
    for item in BASE_URLS:
        data = []
        fpath = BASE_DIR.joinpath(item[0])
        if not fpath.parent.exists():
            fpath.parent.mkdir(parents=True)
        for link_index in range(2, int(item[1])):
            crawlable = Crawlable(item[link_index])
            crawlable.retrieve()
            tags = crawlable._soup.find_all(attrs={"class":"quoteText"})
            for tag in tags:
                array = tag.text.split("\n")
                for string in array: 
                    if (len(string) > 5 and not tag.script): data.append(string)
        data = data[::2]
        write(fpath, data)
