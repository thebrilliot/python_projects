# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 09:58:19 2020

@author: lando

Grabbing the ages of the House Representatives from
https://www.worldpress.org/article.cfm/current-members-of-the-house-of-representatives
"""

import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

def make_soup(url: str):
    html = urlopen(url).read()
    soup = bs(html)
    return 

soup = make_soup('https://www.worldpress.org/article.cfm/current-members-of-the-house-of-representatives')
print(soup.prettify())
content = soup.findAll('div', {'id':'content'})[0]
ps = content.findAll('p')

def house_rep(text: str, party: str) -> dict:
    get_data = re.compile('(?P<state>.*?)\s?\((?P<district>.*?)\)\:?\s?(?P<name>.*?)\,.*?[Cc]urrent\sage\:\s?(?P<age>\d{2})')
    m = get_data.match(text)
    rep = {'name':m.group('name'),'age':m.group('age'),'state':m.group('state'),'district':m.group('district'),'party':party}
    return rep

party = ''
record = False
l=[]
a = ''
for i, line in enumerate(ps):
    if (line.text == 'DEMOCRATS'):
        party = 'D'
    if (line.text == 'REPUBLICANS'):
        party = 'R'
        record = False
    if (line.text == 'DELEGATES (They have a voice on the floor, but no voting power.)'):
        record = False
        
    a = line.text
    if (record):
        print(i)
        l.append(house_rep(line.text,party))
        
    if ((line.text == 'DEMOCRATS') | (line.text == 'REPUBLICANS')):
        record = True
    # input(a)                
    
df = pd.DataFrame(l)
df.to_csv('C:/lando/Desktop/Python/house_reps.csv')