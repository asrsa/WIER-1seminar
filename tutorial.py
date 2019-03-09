from queue import LifoQueue

import psycopg2
from config import config
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

conn = None
frontier = LifoQueue()
visited = set()

try:
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    # insert into table
    #sql = """INSERT INTO crawldb.data_type(code) VALUES(%s);"""
    #cur.execute(sql, ("asd", ))
    #conn.commit()

    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://evem.gov.si')
    html = driver.page_source
    driver.quit()
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    print('\n\n')
    print(soup.title)
    print('\n')
    for link in soup.find_all('a'):
        #print(link.get('href'))
        if 'http' in str(link.get('href')) and not (str(link.get('href')) in visited) and 'gov.si' in str(link.get('href')):
            frontier.put(link.get('href'))
            visited.add(link.get('href'))

    while not frontier.empty():
        item = frontier.get()
        print(item)



    #fetch all
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
