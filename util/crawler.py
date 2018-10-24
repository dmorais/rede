import requests
from bs4 import BeautifulSoup
import re
import sys
import time

def get_publication(list_authors):
    '''

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

                    _splitter(record[0], div_layout5.getText(separator=u' ').strip())

        time.sleep(30)
    return True


def _splitter(author, pub):
    record = pub.strip().split(' . ')

    if len(record) <= 1:
        full_name = author.split(' ')
        with open("-".join(full_name) + "-problems_with_citation.txt", 'a') as f:
            line = author + '|' + pub
            f.write(line)
            f.write("\n\n")
            return True

    title = record[1].split('.')
    _normalize_names(author + "|" + record[0] + "|" + title[0] + "| " + "".join(title[1:]))

    return True



def _normalize_names(pub):
    '''

    :param pub: string in the format specified by the function splitter
    :return:
    '''

    regexes = (
        r' D[AEIOU]\s+',
        r'-',
        r'DOS',
        r'DAS'

    )

    regex = re.compile("|".join(regexes), re.IGNORECASE)
    record = pub.strip().split("|")

    authors = record[1].split(';')
    authors_corrected = list()


    for author in authors:

        # Capitalize and Remove preposition and hifens from names
        author = re.sub(regex, " ", author.strip().upper()).strip()

        # Convert Author to the format Last_name, Initials.
        names = author.split(',')

        # Sometimes the authorship appears without ',' :(
        # In this case check the len of names and split by space

        if len(names) == 1:
            names = author.split(' ')

        # Check if last_name is made up by two names
        last_names = names[0].split(' ')

        # Convert last_name last_name, name to last_name, name last_name
        if len(last_names) > 1:
            names[0] = last_names[-1]
            names[1] += " " + "  ".join(last_names[:-1])


        # Fix cases where fisrt_names appear without space M.G
        names[1] = names[1].replace('.', '. ')

        first_names = names[1].strip().split(' ')
        list_of_correct_names = list()


        for first_name in first_names:

            if first_name == '':
                continue
            else:
                if len(first_name) == 1:
                    first_name += '.'
                    list_of_correct_names.append(first_name)
                elif len(first_name) > 2:
                    first_name = first_name[0] + '.'
                    list_of_correct_names.append(first_name)
                else:
                    list_of_correct_names.append(first_name)

        names[1] = " ".join(list_of_correct_names)

        names_corrected = list()
        names_corrected.append(" ".join(names))

        # put Everything back (correcte list of names)
        authors_corrected.append("".join(names_corrected))

    # put Everything back (correcte list of records)
    record[1] = "; ".join(authors_corrected)

    print("|".join(record), end="\n\n")

    return True

