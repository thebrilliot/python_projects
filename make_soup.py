# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:22:28 2020

@author: lando
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

def make_soup(url):
    site = urlopen(url)
    html = site.read()
    site.close()
    html_soup = soup(html,'html.parser')
    return html_soup

# html_soup = make_soup('https://brhd.org/coronavirus/')
# print(html_soup.findAll('a'))