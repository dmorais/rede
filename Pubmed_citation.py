from util.pubmedcrawler import get_pmid
from util.util import get_titles, ensure_dir
import sys
import os


def main():
    if (len(sys.argv) != 3) or sys.argv[1] == "-h":
        print("\nThis script fetches citations from pubmed base on "
              "its title and parses the output\nUsage\n\npython " + sys.argv[0] + " file_name author_name\n\n")
        sys.exit()

    dir_path = os.path.join(os.getcwd(), "pubmed_problems")
    ensure_dir(dir_path)

    file_name = sys.argv[1]
    author = sys.argv[2]

    titles = get_titles(file_name)
    get_pmid(titles, author, dir_path)


if __name__ == '__main__':
    main()
