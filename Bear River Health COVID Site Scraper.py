# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:18:43 2020

@author: lando
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from datetime import date
import re
#import time

#while (1):
    
#Importing the html code
website = 'https://brhd.org/coronavirus/'
opensite = urlopen(website)
site_html = opensite.read()
opensite.close()

#Turning the code into a parseable object
covid_soup = soup(site_html, 'html.parser')

#print(covid_soup)

#Locating the data from the tables
box1 = covid_soup.findAll('div', {'class':'et_pb_column et_pb_column_3_5 et_pb_column_47 et_pb_css_mix_blend_mode_passthrough'})
box2 = covid_soup.findAll('div', {'class':'et_pb_column et_pb_column_2_5 et_pb_column_48 et_pb_css_mix_blend_mode_passthrough et-last-child'})
dateBox = covid_soup.findAll('div', {'class':'et_pb_module et_pb_text et_pb_text_70 et_pb_text_align_left et_pb_bg_layout_light'})
box1 = box1[0] #Turning the results from lists back into a parseable object
box2 = box2[0]
dateBox = dateBox[0]
#type(box1)

#Extracting the data from the tables
by_category = [[],[],[],[],[]]
i = 0
for row in [0,1,2,3,4]:
    for cell in box1.findAll('div',{'class': 'et_pb_text_inner'}):
        if (i == row):
            by_category[row].append(cell.text)
        if (i == 4):
            i = 0
        else:
            i += 1

#print(by_category)
        
by_age = [[],[],[],[]]
i = 0
box2.findAll('div',{'class': 'et_pb_text_inner'})
for row in [0,1,2,3]:
    for cell in box2.findAll('div',{'class': 'et_pb_text_inner'}):
        if (i == row):
            by_age[row].append(cell.text)
        if (i == 3):
            i = 0
        else:
            i += 1

#print(by_age)

#Combining the data into rows that can be added to the .csv file
update = [[],[],[]]
for row in [0,1,2]:
    update[row]=by_category[row+1]
    update[row].extend(by_age[row+1][1:])
#print(update)

findDate = re.compile('Last Updated:.*?(?P<month>[A-Z][a-z]+)\s(?P<day>\d{1,2}),\s(?P<year>\d{4})')
for cell in (dateBox.findAll('div',{'class':'et_pb_text_inner'})):
    findDate = findDate.search(cell.text)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
month = months.index(findDate.group('month')[0:3])+1
day = int(findDate.group('day'))
year = int(findDate.group('year'))

#Creating a writer to append the new data
csv = 'bear_river_cases.csv'
write_update = open(csv,'a',encoding='utf-8')
today = date.today() #This took forever to figure out
line = ''
for row in update:
    for cell in row:
        line += cell + ','
    if (isinstance(findDate,re.Match)):
        line += str(month) + '-' + str(day) + '-' + str(year) + '\n'
    else:
        line += str(today.month)+'-'+str(today.day)+'-'+str(today.year)+'\n'
print(line)
write_update.write(line)
write_update.close()

 #   time.sleep(86400)