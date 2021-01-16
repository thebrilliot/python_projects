# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 23:32:21 2020

@author: lando

Just scraping some tables. No biggie.
Shouldn't need to use this ever again.
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

url = 'https://www.epa.gov/coalash/list-publicly-accessible-internet-sites-hosting-compliance-data-and-information-required'
open_html = urlopen(url)
site_html = open_html.read()
site_soup = soup(site_html,'html.parser')

table_soup = site_soup.findAll('table',{})

plants = []
for table in table_soup:
    for row in table.findAll('tr',{}):
        plant = []
        for cell in row.findAll('td',{}):
            plant.append(cell.text)
        plants.append(plant)
        
print(plants)

csv = 'power_plant_compliance.csv'
write_csv = open(csv,'w',encoding='utf-8')

line = ''
for plant in plants:
    for datum in plant:
        line += datum + ','
    line = line[:-1]+'\n'
    print(line)

write_csv.write(line)
write_csv.close()