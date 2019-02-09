"""Main entrypoint for scraping script."""
from argparse import ArgumentParser
from crawler import crawler
from parser import parser


def create_arg_parser():
    """Create the command line argument parser."""
    arg_parser = ArgumentParser("A CLI for scraping and parsing data")
    return arg_parser


def main():
    """Main entrypoint to start the crawler."""
    arg_parser = create_arg_parser()
    arg_parser.add_argument(
        "--all",
        action="store_true",
        help="Crawl all content"
    )
    arg_parser.add_argument(
        "--no-cache",
        dest="no_cache",
        action="store_true",
        help="Ignore cache and re-crawl"
    )
    arg_parser.add_argument(
        "--parse",
        action="store_true",
        help="Parse crawled content; will not retrieve any resources."
    )
    arg_parser.add_argument(
        "--gutenberg",
        action="store_true",
        help="Crawl the Gutenberg Project for content"
    )
    arg_parser.add_argument(
        "--genius",
        action="store_true",
        help="Crawl the Genius Lyrics for content"
    )
    args = arg_parser.parse_args()
    if args.parse:
        parser.parse(**vars(args))
    else:
        crawler.crawl(**vars(args))


if __name__ == "__main__":
    main()
