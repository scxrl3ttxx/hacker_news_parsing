import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import time
from random import randint


conn = sqlite3.connect('hacker_news_articles.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              link TEXT NOT NULL)''')


file = open('hacker_news_articles.csv', 'w', newline='', encoding='utf-8')
obj = csv.writer(file)
obj.writerow(['Title', 'Link'])

url = 'https://news.ycombinator.com/news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

pages = 5
for page in range(pages):
    if page == 0:
        url1 = url
    else:
        url1 = f'{url}?p={page + 1}'

    response = requests.get(url1, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', id='hnmain')
    rows = table.find_all('tr', class_='athing')

    for row in rows:
        title_tag = row.find('span', class_='titleline')
        if title_tag is not None:
            title = title_tag.text.strip()
            link = title_tag.find('a')['href']

            c.execute('''INSERT INTO articles (title, link)
                         VALUES (?, ?)''', (title, link))
            print(title, link)
            
            obj.writerow([title, link])

    time.sleep(randint(15, 20))

conn.commit()
conn.close()

file.close()