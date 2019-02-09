# Speechli Scraper

Archive for all scraped speechli data.

To run the crawler using docker:

```sh
docker-compose build
docker-compose up
```

To run a specific command within the docker container:

```sh
docker-compose run --rm speechli-crawler <command>

# Example of running the gutenberg parser without the cache:
docker-compose run --rm speechli-crawler \
    python main.py --gutenberg --parser --no-cache
```

To run the crawler locally:

```sh
# Setup environment (requires Python 3.6+)
python -m venv speechli-scraping-env
git clone https://github.com/treyhakanson/speechli-scraping speechli-scraping-env

# Activate environment
cd speechli-scraping-env
source bin/activate

# Install requirements
cd speechli-scraping
pip install -r requirements.txt

# Navigate to working directory and run crawler
cd src
python main.py --all
```
