import requests
from bs4 import BeautifulSoup
import re
import sys
import os
from util.crawler import normalize_names


def get_pmid(references, author, dir_path):
    '''
    This function fetches a full citation from NCBI pubmed.
    :param references: (list)  article titles
    :param author: (str) full author name (str)
    :param dir_path: (str) path to output dir
    :return: True
    '''

    regex = re.compile(" - PubMed - NCBI")
    comma_regex = re.compile(',')

    full_name = author.split(' ')
    file_prob = open(os.path.join(dir_path, "_".join(full_name) + "_pubmed_error.txt"), 'a')

    for record in references:

        len_record = list()
        data = requests.get('https://www.ncbi.nlm.nih.gov/pubmed/?term=' + record)
        soup = BeautifulSoup(data.text, 'html.parser')

        # Get and parse title

        # Get an alternative title in the p tag which is not the same as the search
        if soup.find('p', class_="title"):
            title = soup.find('p', class_="title").text

        else:
            # Real full title
            if soup.find("title"):
                title = soup.find("title").text
            else:
                title = None

        title = re.sub(regex, " ", title).strip()
        len_record.append(len(title))

        # Get and parse co-authors
        coauthors = soup.find('div', class_="auths").text if soup.find('div', class_="auths") else ''
        coauthors = re.sub(comma_regex, ";", coauthors).strip()
        coauthors_list = coauthors.split(';')
        fixed_list = list()

        # Fix cases where initials are not separated be . or space
        for person in coauthors_list:
            names = person.strip().split(' ')
            if len(names[-1]) == 2 and 'Jr' not in names[-1]:
                names[-1] = ". ".join(list(names[-1])) + "."

            person = " ".join(names)
            fixed_list.append(person)

        coauthors = ";".join(fixed_list)

        len_record.append(len(coauthors))

        # Get and parse journal
        journal = soup.find('div', class_="cit").text if soup.find('div', class_="cit") else ''
        len_record.append(len(journal))

        # Check is title is actually right
        if record.upper() not in title.upper() or any(x == 0 for x in len_record):
            citaton = record + "|" + author + "|" + coauthors + "|" + title + "|" + journal + "\n\n"
            file_prob.write(citaton)

        else:
            print("Normalizing citation")
            citaton = author + "|" + coauthors + "|" + title + "|" + journal
            normalize_names(citaton, os.path.join(os.getcwd(), "scrapper_citations"))

    file_prob.close()

    return True
