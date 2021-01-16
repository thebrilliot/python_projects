 # -*- coding: utf-8 -*-
"""
Spyder Editor

Saving an HTML file to your computer and reading it from there.
"""
from bs4 import BeautifulSoup as soup

filename = 'Genome - Wikipedia.html'
f = open(filename, encoding='utf-8')
new_soup = soup(f, 'html.parser')
print(new_soup.h1)

genome_table = new_soup.findAll('table',{'class': 'wikitable sortable'})