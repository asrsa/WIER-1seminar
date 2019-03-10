from builtins import print

import psycopg2
import requests
import datetime

from config import config
from urllib.parse import urlparse


conn = None
seedPages = ['https://e-uprava.gov.si', 'http://evem.gov.si',
             'https://podatki.gov.si', 'http://e-prostor.gov.si']


def siteID(domain, conn):
    curr = conn.cursor()
    sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
    cur.execute(sql, (domain, ))
    id = cur.fetchone()[0]

    return id

def getSitemap(robots):
    for line in robots.splitlines():
        if "sitemap" in line:
            smap = requests.get(line.split(' ')[1])
            return smap.text


for seed in seedPages:
    print('Processing ' + seed)
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        robots = None
        sitemap = None

        responseRobots = requests.get(seed + '/robots.txt')
        if responseRobots.status_code == 200:
            robots = responseRobots.text
            sitemap = getSitemap(robots)


        response = requests.get(seed)
        parsed_uri = urlparse(seed)
        domain = '{uri.netloc}'.format(uri=parsed_uri)

        # insert into table
        sql = """INSERT INTO crawldb.site(domain, robots_content, sitemap_content) 
                    SELECT %s, %s, %s
                    WHERE NOT EXISTS (
                    SELECT 1 FROM crawldb.site WHERE domain=%s
                );"""

        cur.execute(sql, (domain, robots, sitemap, domain))
        conn.commit()

        pageTypeCode = "FRONTIER"

        htmlContent = None
        if "html" in response.headers['content-type']:
            htmlContent = response.text


        # insert into table
        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time) 
                VALUES(%s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (siteID(domain, conn), pageTypeCode, seed, htmlContent, response.status_code, datetime.datetime.now()))
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

