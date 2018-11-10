import argparse
from util.util import get_list_autor_id, ensure_dir
from util.crawler import get_publication
import sys
import os






def main():
    parser = argparse.ArgumentParser(
        description="A tool to Extract information from Lattes platform")

    parser.add_argument('-f', '--file', action="store",
                        help='A csv file containing a list of Lattes names and/or Lattes id',
                        required=True)

    parser.add_argument('-p', '--pub', action='store_true',
                        help="Given a list of Lattes id extract the list of publications of an CV",
                        required=False)

    parser.add_argument('-d', '--dir', action='store_true',
                        default=os.getcwd(),
                        help="A path to the output of scrapper. If none provide use current working dir ",
                        required=False)

    args = parser.parse_args()
    if args.pub:

        dir_path = os.path.join(args.dir,"scrapper_citations")
        ensure_dir(dir_path)

        list_authors = get_list_autor_id(args.file)
        get_publication(list_authors,dir_path)


if __name__ == '__main__':
    main()
