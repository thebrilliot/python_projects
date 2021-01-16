# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:26:09 2020

@author: lando

Scraping non-table data
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re

wiki_url = "https://en.wikipedia.org/wiki/Genome"
wiki_data = urlopen(wiki_url)
wiki_html = wiki_data.read()
wiki_data.close()

page_soup = soup(wiki_html, 'html.parser')
references_list_raw = page_soup.findAll('ol',{'class': 'references'})
print(references_list_raw)

references_list = references_list_raw[0].findAll('li',{})

http = re.compile('http')
all_references = []
for list_item in references_list:
    references = []
    for link in list_item.findAll('a',{}):
        if (isinstance(http.match(link['href']), re.Match)):
            all_references.append(link['href'])

print(all_references)
# Should have only valid http:// and https:// URLs now