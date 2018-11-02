import sys
from util.crawler import normalize_names

def main():

    if (len(sys.argv) != 2) or sys.argv[1] == "-h":
        print("Usage:\n\n  python " + sys.argv[0] + " <author-problems_with_citation.txt>\n\n"
                                                "  The file author-problems_with_citation.txt is automatically create by"
                                                " Scrapper.py" )
        sys.exit()

    file_name = sys.argv[1]

    with open(file_name, 'r') as f:

        for line in f:

            if line.strip():
                print(line)
                normalize_names(line.strip())



if __name__ == '__main__':
    main()