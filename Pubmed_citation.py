from util.pubmedcrawler import get_pmid
from util.util import get_titles, ensure_dir
import sys
import os
from subprocess import call


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

    # # Traverse the pubmed_results and call Fix_prombles to put the citation in the right format
    # for _, _, file_list in os.walk(dir_path):
    #     for fname in file_list:
    #         if '_pubmed.txt' in fname:
    #             print('Normalizing Pubmed Files')
    #             call(['python', os.path.join(os.getcwd(), 'Fix_problems_with_citation.py'), os.path.join(dir_path, fname)])




if __name__ == '__main__':
    main()
