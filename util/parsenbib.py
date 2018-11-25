import os
from util.crawler import normalize_names
from util.util import  get_files_names


def parse_enw(dir_name):
    author_full_name = (os.path.basename(dir_name)).replace("_", ' ')

    pub = dict()
    file_names = get_files_names(dir_name)
    for file_name in file_names:
        with open(os.path.join(dir_name,file_name), 'r') as file_obj:
            for line in file_obj:
                if line.startswith('%T'):
                    pub['title'] = line.replace('%T ','').strip()
                elif line.startswith('%J'):
                    pub['journal'] = line.replace('%J ','').strip()
                elif line.startswith('%V'):
                    pub['volume'] = 'v '+ line.replace('%V ','').strip()
                elif line.startswith('%P'):
                    pub['page'] = 'p '+ line.replace('%P ','').strip()
                elif line.startswith('%D'):
                    pub['year'] = line.replace('%D ','').strip()
                elif line.startswith('%A'):
                    if 'author' in pub.keys():
                       pub['author'].append(line.replace('%A ','').strip())
                    else:
                        pub['author'] = [line.replace('%A ','').strip()]

    print("Normalizing citation")
    citaton = author_full_name + "|" + "; ".join(pub['author']) + "|" + pub['title'] + "|" + pub['journal'] + ", " + pub['volume'] + ", " + pub['page'] + " , " + pub['year']
    normalize_names(citaton, os.path.join(os.getcwd(), "scrapper_citations"))