import argparse
from util.util import get_list_autor_id
from util.crawler import get_publication
import sys


def main():
    parser = argparse.ArgumentParser(
        description="A tool to Extract information from Lattes platform")

    parser.add_argument('-f', '--file', action="store",
                        help='A text file containing a list of Lattes names and/or Lattes id',
                        required=True)

    parser.add_argument('-p', '--pub', action='store_true',
                        help="Given a list of Lattes id extract the list of publications of an CV")

    args = parser.parse_args()

    if hasattr(args, 'pub'):
        list_authors = get_list_autor_id(args.file)
        get_publication(list_authors)


if __name__ == '__main__':
    main()
