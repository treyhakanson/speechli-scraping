"""Genius sub-crawler."""
import csv
from .constants import DATA_DIR
from .crawlable import Crawlable


BASE_DIR = DATA_DIR.joinpath("genius")
BASE_URLS = (
    (
        "lyrics/PostMalone/index.csv",
        "https://genius.com/artists/Post-malone"
    ),
    (
        "lyrics/Drake/index.csv",
        "https://genius.com/artists/Drake"
    ),
    (
        "lyrics/Logic/index.csv",
        "https://genius.com/artists/Logic"
    ),
    (
        "lyrics/TravisScott/index.csv",
        "https://genius.com/artists/Travis-scott"
    ),
    (
        "lyrics/XXXTentacion/index.csv",
        "https://genius.com/artists/Xxxtentacion"
    ),
    (
        "lyrics/G-Eazy/index.csv",
        "https://genius.com/artists/G-eazy"
    ),
    (
        "lyrics/Eminem/index.csv",
        "https://genius.com/artists/Eminem"
    ),
    (
        "lyrics/LilWayne/index.csv",
        "https://genius.com/artists/Lil-wayne"
    ),
    (
        "lyrics/SkiMask/index.csv",
        "https://genius.com/artists/Ski-mask-the-slump-god"
    ),
    (
        "lyrics/KanyeWest/index.csv",
        "https://genius.com/artists/Kanye-west"
    ),

)


def setup():
    """Setup the directories for crawling Genius."""
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)


def clean(link):
    """Clean links."""
    return link.get("href")


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
    """Retrieve the genius indexes."""
    setup()
    for loc, url in BASE_URLS:
        fpath = BASE_DIR.joinpath(loc)
        if not fpath.parent.exists():
            fpath.parent.mkdir(parents=True)
        crawlable = Crawlable(url)
        crawlable.retrieve()
        data = [(clean(link),) for link in crawlable.parse("div > .mini_card")]
        write(fpath, data)
