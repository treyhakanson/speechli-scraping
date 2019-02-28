"""Genius sub-crawler."""
import re
import csv
from .constants import DATA_DIR
from .crawlable import Crawlable


BASE_DIR = DATA_DIR.joinpath("genius")
BASE_URLS = []
# BASE_URLS = (
#     (
#         "lyrics/PostMalone/index.csv",
#         "https://genius.com/artists/Post-malone"
#     ),
#     (
#         "lyrics/Drake/index.csv",
#         "https://genius.com/artists/Drake"
#     ),
#     (
#         "lyrics/Logic/index.csv",
#         "https://genius.com/artists/Logic"
#     ),
#     (
#         "lyrics/TravisScott/index.csv",
#         "https://genius.com/artists/Travis-scott"
#     ),
#     (
#         "lyrics/XXXTentacion/index.csv",
#         "https://genius.com/artists/Xxxtentacion"
#     ),
#     (
#         "lyrics/G-Eazy/index.csv",
#         "https://genius.com/artists/G-eazy"
#     ),
#     (
#         "lyrics/Eminem/index.csv",
#         "https://genius.com/artists/Eminem"
#     ),
#     (
#         "lyrics/LilWayne/index.csv",
#         "https://genius.com/artists/Lil-wayne"
#     ),
#     (
#         "lyrics/SkiMask/index.csv",
#         "https://genius.com/artists/Ski-mask-the-slump-god"
#     ),
#     (
#         "lyrics/KanyeWest/index.csv",
#         "https://genius.com/artists/Kanye-west"
#     ),
#
# )


def setup():
    """Setup the directories for crawling Genius."""
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)
    define_structure()


def define_structure():
    """Creating structure containing artists and respective links"""
    fpath = BASE_DIR.joinpath("lyrics/artist.txt")

    with fpath.open(mode="r") as f:
        for artist in f:
            artist = artist[:-1]
            print(artist)
            file = "lyrics/" + artist + "/index.csv"
            url = "https://genius.com/artists/" + artist
            t = [file, url]
            BASE_URLS.append(t)
    print(f"\tSuccessfully created artist list.")



def clean(link):
    """Clean links."""
    return link.get("href")


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


def get_title(index_url):
    """Get the title of the song based on the index link."""

    crawlable = Crawlable(index_url)
    crawlable.retrieve()
    if crawlable.success:
        title = crawlable.parse("h1.header_with_cover_art-primary_info-title")[0].get_text()
        for char in '<>"|*?./;:':
            title=title.replace(char,'')

    return title


def retrieve_index(no_cache=False, **kwargs):
    """Retrieve the genius indexes."""
    setup()
    #for loc, url in BASE_URLS:
    for item in BASE_URLS:
        loc = item[0]
        url = item[1]
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
        if crawlable.success:
            data = [(clean(link),) for link in crawlable.parse("div > .mini_card")]
            write(fpath, data)
            print(f"\tSuccessfully retrieved index.")
        else:
            print(f"\tNo content available.")


def retrieve_from_index(no_cache=False, **kwargs):
    """Retrieve the lyrics from the index."""
    #for loc, url in BASE_URLS:
    for item in BASE_URLS:
        loc = item[0]
        url = item[1]
        fpath = BASE_DIR.joinpath(loc)
        with fpath.open(mode="r") as csvfile:
            csvreader = csv.reader(
                csvfile,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL
            )
            for row in csvreader:
                index_url = row[0]
                title = get_title(index_url)
                song_fpath = fpath.parent.joinpath(f"{title}.txt")
                print(
                    f"{index_url} -> {song_fpath}"
                )
                if not no_cache and song_fpath.exists():
                    # If we are using the cache and the result exists, skip
                    print(f"\tUsing cached results.")
                    continue
                crawlable = Crawlable(index_url)
                crawlable.retrieve()
                artist = crawlable.parse(".header_with_cover_art-primary_info-primary_artist")[0].get_text()
                text = crawlable.parse(".lyrics")[0].get_text()
                write(song_fpath, "Title:" + title+"\n"+ "Artist:" + artist + text)
                print(f"\tSuccessfully retrieved lyrics.")


def fetch(**kwargs):
    """Fetch the indexes, and the retrieve the lyrics from those indexes."""
    retrieve_index(**kwargs)
    retrieve_from_index(**kwargs)
