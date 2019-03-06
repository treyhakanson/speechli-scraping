import re
import json
from pathlib import Path


def main():
	fpath = Path('./data/goodreads/quotes')
	for subpath in fpath.iterdir():
		with subpath.open(mode='r') as f:
			data = json.load(f)
		content = '\n'.join(data)
		author = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', subpath.name.split('.json')[0]))
		doctype = 'quote'
		title = f'{author} Quotes'
		cleaned_data = {'content': content, 'author': author, 'type': doctype, 'title': title}
		with subpath.open(mode='w') as f:
			json.dump(cleaned_data, f)


if __name__ == '__main__':
	main()
