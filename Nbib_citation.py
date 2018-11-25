
from util.util import get_dirs, get_files_names, ensure_dir
from util.parsenbib import parse_enw
import sys
import os
import argparse



def main():
    parser = argparse.ArgumentParser(
        description="A tool to Extract information from Lattes platform")

    parser.add_argument('-c', '--create', action="store_true",
                        help='A csv file containing a list of Lattes names and/or Lattes id',
                        required=False)

    parser.add_argument('-p', '--parse', action='store_true',
                        help="Given a list of Lattes id extract the list of publications of an CV",
                        required=False)

    parser.add_argument('-d', '--dir', action='store_true',
                        default=os.getcwd(),
                        help="A path to the output of scrapper. If none provide use current working dir ",
                        required=False)

    args = parser.parse_args()
    if args.create:
        print("Getting author's name from files with problems")
        author_names = get_files_names(os.path.join(os.getcwd(), 'pubmed_problems'), prob=True)

        for name in author_names:
            dir_path = os.path.join(os.getcwd(), os.path.join("nbib", name))
            ensure_dir(dir_path)

    elif args.parse:
        nbib_dir = get_dirs(os.path.join(os.getcwd(), "nbib"))
        for directory in nbib_dir:
            parse_enw(os.path.join(os.getcwd(), os.path.join("nbib", directory)))








if __name__ == '__main__':
    main()