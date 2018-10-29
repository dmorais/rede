def get_list_autor_id(file_name):
    '''

    :param file_name: A tsv file with a list of author lattes id
    :return: a list of tuples (author_name,id)

    '''
    with open(file_name, 'r') as file_obj:

        return [(line[0], line[1]) for line in (line.strip().split(",") for line in file_obj if line.strip())]
