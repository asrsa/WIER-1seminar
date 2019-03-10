import os
from queue import LifoQueue

import psycopg2
import wget as wget

from config import config
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

conn = None
frontier = LifoQueue()
visited = set()

# database code
"""
try:
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    # insert into table
    #sql = """"""INSERT INTO crawldb.data_type(code) VALUES(%s);""""""
    #cur.execute(sql, ("asd", ))
    #conn.commit()

    # fetch all
    print('\n')
    cur.execute("SELECT * FROM crawldb.data_type")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # close the communication with the PostgreSQL
    cur.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')
"""

# init headless browser
chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)

# frontier init
frontier.put('http://evem.gov.si')

path = input('Enter folder name to download the media: ')
if not os.path.exists(path):
    os.mkdir(path)

while not frontier.empty():
    # deque from LIFO
    urlLink = frontier.get()
    # store into visited set
    visited.add(urlLink)

    # url being processed
    print(urlLink)

    # obtain page source
    driver.get(urlLink)
    html_source = driver.page_source

    soup = BeautifulSoup(html_source, 'html.parser')

    # extract <a> tags only
    for link in soup.find_all('a'):
        # print(link.get('href'))
        url = str(link.get('href'))
        # do not store JPG, PDF, PPT, MP4
        if '.mp4' in url or '.ppt' in url or '.doc' in url or '.pdf' in url or '.rar' in url or '.zip' in url:
            try:
                media = wget.download(url, out=str(path + '/'))
            except:
                pass
            continue
        if 'http' in url and 'gov.si' in url and url not in visited and 'jpg' not in url and 'ppt' not in url \
                and 'mp4' not in url and 'pdf' not in url and '.zip' not in url and '.rar' not in url and '.xml' not in url \
                and '.doc' not in url and '@' not in url and 'linkedin' not in url and 'facebook' not in url and 'evem' in url:
            frontier.put(link.get('href'))

driver.quit()

# print the number of visited urls
print(len(visited))
# print visited urls
for link in visited:
    print(link)
