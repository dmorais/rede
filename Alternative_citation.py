import sys
import os


def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        print("Creating", dir_path)
        os.makedirs(dir_path)

    return True


def create_list_of_citations(file_name, dir_path, author):
    citations = dict()
    with open(file_name, 'r') as f:
        for line in f:
            if not line.strip():
                continue

            records = line.strip().split("|")
            names = records[1].split(";")

            for name in names:

                name = name.strip()
                last_names = name.split(' ')

                if last_names[0] in citations.keys():
                    citations[last_names[0]].add(name)
                else:
                    citations[last_names[0]] = {name}

    with open(os.path.join(dir_path, author + "_Alternative_citation.txt"), 'a') as f:
        for k, v in citations.items():

            # Print only if there is an alternative citation
            if len(v) > 1:
                text = k + ' : ' + '; '.join(v)
                f.write(text)
                f.write('\n\n')


def main():
    if (len(sys.argv) != 2) or sys.argv[1] == "-h":
        print("Usage:\npython " + sys.argv[0] + " <File created by Scapper.py>\n"
                                                "The script now creates a dir from the CWD and writes to"
                                                "files named after the author.")
        sys.exit()

    dir_path = os.path.join(os.getcwd(), "alternative_citations")

    ensure_dir(dir_path)

    file_name = sys.argv[1]

    author = os.path.basename(file_name).split('.')

    create_list_of_citations(file_name, dir_path, author[0])


if __name__ == '__main__':
    main()
