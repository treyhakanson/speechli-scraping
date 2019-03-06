import re
import json
from pathlib import Path


def main():
        fpath = Path('./data/genius/raw_data/lyrics.json')
        with fpath.open(mode='r') as f:
                data = json.load(f)
        for song in data:
                title = song['title']
                song['author'] = song['artist']
                del song['artist']
                with open(f'./data/genius/raw_data/{title}.json', 'w') as f:
                        json.dump(song, f)


if __name__ == '__main__':
        main()
