"""Main entrypoint for scraping script."""
from argparse import ArgumentParser
from crawler import crawler


def create_parser():
    """Create the command line argument parser."""
    parser = ArgumentParser("A CLI for scraping data")
    return parser


def main():
    """Main entrypoint to start the crawler."""
    parser = create_parser()
    parser.add_argument(
        "--all",
        action="store_true",
        help="Crawl all content"
    )
    parser.add_argument(
        "--no-cache",
        dest="no_cache",
        action="store_true",
        help="Ignore cache and re-crawl"
    )
    parser.add_argument(
        "--gutenberg",
        action="store_true",
        help="Crawl the Gutenberg Project for content"
    )
    parser.add_argument(
        "--genius",
        action="store_true",
        help="Crawl the Genius Lyrics for content"
    )
    args = parser.parse_args()
    crawler.crawl(**vars(args))


if __name__ == "__main__":
    main()