# Rede


This repo contains a few scripts that can extract parse and analyse a 
network of co-authorship.

# Requirements
```
python 3.6.2 or above

```

## Scripts

* Scrapper.py

```
usage: Scrapper.py [-h] -f FILE [-p]

A tool to Extract information from the Lattes platform

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  A csv file containing a list of Lattes names and
                        Lattes id
  -p, --pub             Given a list of Lattes id extract the list of
                        publications of an CV
                        
                        
# To run
# extract publications

python Scrapper.py -f author-file.tsv -p 

```

* Name_replacer.py - A script to replace the occurrence a string by another string.



```
python Name_replacer.py <file_with_names.txt> <list_of_publications.txt>

# file_with_name.txt - A pipe separated file in the form STRING-TO-BE-REPACED|REPLACEMENT
# list_of_publications.txt - Either the output of the Scrapper.py of a file with strings that needs to 
#be replaced according to the pattern in file_with_name.txt
# Example

python Name_repacer.py examples/file_names.txt examples/extracted_raw_data.txt

```

* Alternative_citation.py - This script creates a file with a list of last names
cited in different forms. It can be used to create the list needed by the 
Name_replacer.py.

A example of its output is in examples/alternative_citation.txt

```
python Alternative_citation.py -h 

Usage:
python Alternative_citation.py <File created by Scapper.py>




```

* Pubmed_citation.py - This script fetches PubMed records based on their title and parses them.

```
python  Pubmed_citation.py file_name "author_name"

# File_name contains a list of article titles retrieved from the citations_with_problems file
# Autor_name is the full author_name as a string (surrounded by double quotes)

# Notes: The script updated the record in scrapper_citation/autor_name.txt and creates a 
pubmed_problems/autor_pubmed_error.txt

```

* Nbib_citations.py - This script is used to parse the ewn (endnote output)
```
usage: Nbib_citation.py [-h] [-c] [-p]

A tool to Parse ewn file (endnote format) and update scrapper.py output

optional arguments:
  -h, --help    show this help message and exit
  -c, --create  A the file directory structure where the ewn files should be
                put. This option should be ranonly once, unless new
                researchers are added to the pubmed_problem dir.
  -p, --parse   Parse all files in the nbib/author dir and update scrapper
                output.

```

How to run
```
# Create dir struture.

# In this mode the script looks inside the dir pubmed_problems and checks which authors still have 
missing citation. It then creates the nbib/author_name . 

# NOTE: You must put the ewn files there.

python Nbib_citation.py -c


# Parse the ewn file. In this mode the script traverse the nbib directory tree and for each author 
it parses the ewn file. 

#The scrapper output file is updated for each publication parsed. 

python Nbib_citation.py -p

```