import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import os
from util.util import ensure_dir


def get_publication(list_authors, dir_path):
    '''
    Fetch Publications from url
    :param dir_path: A path to a directory where scrapper will output the citations
    :param list_authors: list of tuples (name, id)
    :return: True
    '''

    for record in list_authors:
        data = requests.get('http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=' + record[1])
        soup = BeautifulSoup(data.text, 'html.parser')

        for div in soup.find_all('div', {'class': 'artigo-completo'}):
            for div_layout5 in div.find_all('div', {'class': 'layout-cell-pad-5'}):
                unwanted = div_layout5.find('span', {'data-tipo-ordenacao': 'autor'})

                if unwanted is not None:
                    unwanted.extract()

                    unwanted_ano = div_layout5.find('span', {'data-tipo-ordenacao': 'ano'})
                    unwanted_ano.extract()


                    pub = _splitter(record[0], div_layout5.getText(separator=u' ').strip())

                    if isinstance(pub, str):
                        normalize_names(pub,dir_path)

        time.sleep(30)
    return True


def _splitter(author, pub):
    '''
    Split publication record into authors | title | journal

    :param author: full author's name string
    :param pub: publication record string
    :return: a string with author and publication records
    '''
    record = pub.strip().split(' . ')

    if len(record) <= 1:
        _print_problems(author, pub)
        return True

    title = record[1].split('.')
    pub = author + "|" + record[0] + "|" + title[0] + "| " + "".join(title[1:])
    return pub



def normalize_names(pub,dir_path):
    '''
    Remove unwanted char from names and standardize the citation

    :param pub: string in the format specified by the function splitter
    :param dir_path: A path to a directory where scrapper will output the citation
    :return: True
    '''

    # Some publication contain a new line within. It needs to be removed
    new_line_regex = re.compile('\n')
    pub = re.sub(new_line_regex, " ", pub)

    # List of patterns to be removed from authors' names
    regexes = (
        r'\s?D[AEIOU]\s+',
        r'-',
        r'\s+DOS\s+',
        r'\s+DAS\s+',
        r'\s+DE$',
        r'\s+DA$',
        r'\s+DI$'
        r'\s+DO$',
        r'\s+E\s+',
        r'JR',
        r'\d+'

    )

    regex = re.compile("|".join(regexes), re.IGNORECASE)
    record = pub.strip().split("|")

    authors = record[1].split(';')

    for i, author in enumerate(authors):

        # Capitalize and Remove preposition and hifens from names
        author = re.sub(regex, " ", author.strip().upper()).strip()

        # Convert Author to the format Last_name, Initials.
        names = author.split(',')

        # Sometimes the authorship appears without ',' :(
        # In this case check the len of names and split by space
        if len(names) == 1:
            names = author.split(' ')

        # Check if names is not only made up by Initial and names[0] Is not a Inintal
        initial, names = _verify_name_structure(names[:], pub)

        # If initial is True the author's name has a problem. Break the processing of this publication print to problem file
        if initial:
            return True

        names = _isolate_last_name(names[:])

        if len(names) > 1:
            names[1] = _create_initials(names[1])

        authors[i] = " ".join(names)

    record[1] = "; ".join(authors)
    citation = "|".join(record)


    full_name = record[0].split(' ')
    with open( os.path.join(dir_path,"_".join(full_name) + "_citations.txt"), 'a') as f:
        f.write(citation)
        f.write("\n\n")

    return True


def _isolate_last_name(author_name):
    '''
    Isolate last_name from other_names

    :param name: a list of the full author's citation name that was split either by ' ' or by '
    :return: A list in the form [ last_name, other_names]
    '''

    # The author has just one name
    if len(author_name) == 1:
        return author_name
    else:
        last_names = author_name[0].split(' ')

        # Check if last_name is made up by one name
        if len(last_names) == 1:

            # if author_name[0] is only a letter switch by author_name[1]
            if len(author_name[0]) == 1 and len(author_name[1]) > 1:
                author_name[0], author_name[1] = author_name[1], author_name[0].split(' ')[0]

            return author_name

        # last_name is made up by two or more names
        else:
            # check if the last element of last_name list is not just a single letter or an Abbreviation
            if len(last_names[-1]) == 1 or '.' in last_names[-1]:
                author_name[0] = last_names.pop(-2)
                author_name[1] += " " + " ".join(last_names)
                return author_name

            else:
                author_name[0] = last_names.pop()
                author_name[1] += " " + " ".join(last_names)
                return author_name


def _create_initials(author_name):
    '''
    Reduce names to Its initials

    :param author_name: a string with the author names
    :return: a string with the initials of each name followed by a .
    '''

    author_name = author_name.strip().replace('.', '. ')
    names = re.split('\s+', author_name)
    initials = ' '

    for name in names:
        if name != '' and name not in ['DO', 'DOS', 'DA', 'DAS', 'DE', 'DES', 'DI', 'DU']:
            initials += name[0] + '.' + ' '

    return initials


def _print_problems(author, pub):

    dir_path = os.path.join(os.getcwd(),"citations_with_problems")
    ensure_dir(dir_path)

    full_name = author.split(' ')
    with open( os.path.join(dir_path,"_".join(full_name) + "_citations.txt"), 'a') as f:
        line = author + '|' + pub
        f.write(line)
        f.write("\n\n")

    return True


def _verify_name_structure(names, pub_full):
    '''
    Check if names[0] is not in fact a initial.
    Do a swap to names[-1] if it is names[-1]>2 otherwise print as error

    :param names: list with author name split by either space or comma
    :param pub_full: a string containing authors full name|publication record
    :return: a tuple where the first element is a Boolean and the second a list.
    '''

    # Last name is not an Initial return names
    if len(names[0]) > 1 and "." not in names[0]:
        return False, names

    else:
        # If name[-1] is larger than names[0]
        if (len(names[-1]) > 1 and "." not in names[-1]) and (len(names[-1]) > len(names[0])):
            last_name = names.pop(-1)
            names.insert(0, last_name)
            return False, names
        else:
            pub = pub_full.split('|')
            author = pub.pop(0)
            _print_problems(author, "|".join(pub))
            return True, names
