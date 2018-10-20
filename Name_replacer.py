import sys
import re


def get_dict_of_names(file_of_names):
    '''

    :param file_of_names: The file name where field1 is the term to search and field2 the term to replace to
    :return: a dictionary
    '''

    with open(file_of_names, 'r') as file_obj:
        return {line[0]: line[1] for line in (line.strip().split("|") for line in file_obj if line.strip())}


def replace_occurrences(dict_of_names, file_name):

    with open(file_name, 'r') as f:

        for line in f:

            for name in dict_of_names.keys():
                if name in line:
                    line = line.replace(name, dict_of_names[name])

            print(line.strip())

def main():

    file_of_names = sys.argv[1]
    reference_file_names = sys.argv[2]

    dict_of_names = get_dict_of_names(file_of_names)
    replace_occurrences(dict_of_names,reference_file_names)




if __name__ == '__main__':
    main()
