import requests
from bs4 import BeautifulSoup


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

                    splitter(record[0], div_layout5.getText(separator=u' ').strip())
    return True


def splitter(author, pub):
    record = pub.strip().split(' . ')
    title = record[1].split('.')
    print(author + "|" + record[0] + "|" + title[0] + "| " + "".join(title[1:]))

    return True
