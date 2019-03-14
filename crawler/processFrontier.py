import hashlib
from builtins import print
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dblib import *
from config import config
from urllib.parse import urlparse
import psycopg2
import requests
import datetime


def siteID(domain, conn):
    cur = conn.cursor()
    sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
    cur.execute(sql, (domain, ))
    id = cur.fetchone()[0]

    return id


def getSitemap(robots):
    for line in robots.splitlines():
        if "sitemap" in line:
            smap = requests.get(line.split(' ')[1])
            return smap.text


def processFrontier(seed):
    print('Processing ' + seed)
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        robots = None
        sitemap = None

        response = requests.get(seed)
        parsed_uri = urlparse(seed)
        domain = '{uri.netloc}'.format(uri=parsed_uri)

        # TODO: if domain !exists insert new (use dblib.getSiteId)
        if getSiteId(domain) is None:
            responseRobots = requests.get(seed + '/robots.txt')
            if responseRobots.status_code == 200:
                robots = responseRobots.text
                sitemap = getSitemap(robots)

            sql = """INSERT INTO crawldb.site(domain, robots_content, sitemap_content) 
                        SELECT %s, %s, %s
                        WHERE NOT EXISTS (
                        SELECT 1 FROM crawldb.site WHERE domain=%s
                    );"""
            cur.execute(sql, (domain, robots, sitemap, domain))
            conn.commit()

        htmlContent = None
        htmlHash = ''
        if "html" in response.headers['content-type']:
            driver.get(seed)
            htmlContent = driver.page_source
            htmlHash = hashlib.md5(htmlContent.encode()).hexdigest()
        driver.close()

        # TODO: is page duplicate? enter DUPLICATE
        #  Duplicate po page content? Ker page url ima na nivoju baze setan unique_url_index
        sql = """select hash from crawldb.page where hash=%s;"""
        cur.execute(sql, (seed, ))
        # ce najde vsaj en record v tabeli, pomeni, da page ze obstaja -> duplicat
        if cur.fetchone() is None:
            pageTypeCode = "FRONTIER"
        else:
            pageTypeCode = "DUPLICATE"

        # insert into table
        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash) 
                VALUES(%s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (siteID(domain, conn), pageTypeCode, seed, htmlContent, response.status_code, datetime.datetime.now(), htmlHash))
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.IntegrityError):
        print('Url ze obstaja v bazi!')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
