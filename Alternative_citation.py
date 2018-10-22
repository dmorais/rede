import sys



def create_list_of_citations(file_name):

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



    for k,v in citations.items():

        # Print only if there is an alternative citation
        if len(v) > 1:
            print(k + ' : '+ "; ".join(v))


def main():

    if (len(sys.argv) != 2) or sys.argv[1] == "-h":
        print("Usage:\npython " + sys.argv[0] + " <File created by Scapper.py>\n" )
        sys.exit()

    file_name = sys.argv[1]

    create_list_of_citations(file_name)


if __name__ == '__main__':
    main()