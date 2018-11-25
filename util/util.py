import os
def get_list_autor_id(file_name):
    '''

    :param file_name: A tsv file with a list of author lattes id
    :return: a list of tuples (author_name,id)

    '''
    with open(file_name, 'r') as file_obj:
        return [(line[0], line[1]) for line in (line.strip().split(",") for line in file_obj if line.strip())]


def get_titles(file_name):

    with open(file_name, 'r') as file_obj:

        return [line.strip() for line in file_obj if line.strip()]

def ensure_dir(dir_path):

    if not os.path.exists(dir_path):
        print("Creating", dir_path)
        os.makedirs(dir_path)

    else:
        print(dir_path + " already exists")

    return True


def get_dirs(base_dir):

    nbib_dir_list = list()
    for _, sub_dir_list, _ in os.walk(base_dir):
        for sub_dir in sub_dir_list:
            nbib_dir_list.append(sub_dir)

    return nbib_dir_list

def get_files_names(base_dir, prob=False):

    file_names = list()
    for _, _, file_list in os.walk(base_dir):
        for names in file_list:
            if prob:
                names = names.replace("_pubmed_error.txt",'')
            file_names.append(names)


    return file_names

