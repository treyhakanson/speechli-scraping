import re
import json
from pathlib import Path


def main():
	authors = set()
	fpath = Path('./data/goodreads/quotes')
	for subpath in fpath.iterdir():
		author = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', subpath.name.split('.json')[0]))
		authors.add(author)
	fpath = Path('./data/genius/raw_data/lyrics.json')
	with fpath.open(mode='r') as f:
		data = json.load(f)
	for song in data:
		author = song['artist']
		authors.add(author)
	fpath = Path('./data/gutenberg/bookshelf/adventure/parsed')
	for subpath in fpath.iterdir():
		with subpath.open(mode='r') as f:
			data = json.load(f)
		author = data['author']
		authors.add(author)
	fpath = Path('./data/gutenberg/bookshelf/science-fiction/parsed')
	for subpath in fpath.iterdir():
		with subpath.open(mode='r') as f:
			data = json.load(f)
		author = data['author']
		authors.add(author)
	fpath = Path('./data/gutenberg/bookshelf/fantasy/parsed')
	for subpath in fpath.iterdir():
		with subpath.open(mode='r') as f:
			data = json.load(f)
		author = data['author']
		authors.add(author)
	with open('./data/authors.txt', 'w') as f:
		f.write('\n'.join(authors))


if __name__ == '__main__':
	main()