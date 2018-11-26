
from util.util import get_dirs, get_files_names, ensure_dir
from util.parsenbib import parse_enw
import sys
import os
import argparse



def main():
    parser = argparse.ArgumentParser(
        description="A tool to Parse ewn file (endnote format) and update scrapper.py output")

    parser.add_argument('-c', '--create', action="store_true",
                        help='A the file directory structure where the ewn files should be put.  This option should be ran'
                             'only once, unless new researchers are added to the pubmed_problem dir.',
                        required=False)

    parser.add_argument('-p', '--parse', action='store_true',
                        help="Parse all files in the nbib/author dir and update scrapper output.",
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