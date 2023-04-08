import sqlite3

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv

url = "https://www.theverge.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
articles = soup.find_all('div', class_='max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10')

data=[]
conn = sqlite3.connect('theverge_articles.db')
c= conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS dataarticle
                (Title TEXT ,
                 Link TEXT ,
                 Author TEXT ,
                 Date DATE )''')
for article in articles:
    Title = article.find('h2', class_='font-polysans text-20 font-bold leading-100 tracking-1 md:text-24 lg:text-20').text
    Link = article.h2.a['href']
    Author = article.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text.strip()
    Date = article.find('span', class_='text-gray-63 dark:text-gray-94').text

    info = {'Title':Title,'Link':Link,'Author':Author,'Date':Date}
    data.append(info)
    c.execute('''INSERT INTO dataarticle VALUES (?,?,?,?)''', (Title, Link, Author, Date))

filename = datetime.now().strftime('%d%m%y') + '_verge.csv'
with open(filename,'w',newline='',encoding='utf-8') as file:
    writer = csv.DictWriter(file,fieldnames=['Title','Link','Author','Date'])
    writer.writeheader()
    writer.writerows(data)





conn.commit()
print('complete')
c.close()
conn.close()
