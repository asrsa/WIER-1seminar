import hashlib

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from db.dblib import *
from db.config import config
from urllib.parse import urlparse
import psycopg2
import requests
import datetime

# List is used to check if site exists in DB. Instead of performing select operation for every url
# set is generated along with insertion statement to avoid too much 'selecting performance' over and over again
visitedSeed = []

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
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(20)                        # wait 20 seconds, move to next url after timeout


    # wait 3 secs for web to load
    driver.implicitly_wait(3)
    conn = None

    nextPageId = None
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

            # to avoid 'A string literal cannot contain NUL (0x00) characters' exception from postgresql IntegrityError
            # replace all '\x00' characters to '' (blank) in robots and site variable
            if robots is not None:
                robots = robots.replace('\x00', '')
            if sitemap is not None:
                sitemap = sitemap.replace('\x00', '')
            cur.execute(sql, (domain, robots, sitemap, domain))
            conn.commit()

        # obtain seed content
        htmlContent = None
        htmlHash = ''
        if "html" in response.headers['content-type']:
            driver.get(seed)

            htmlContent = driver.page_source
            htmlHash = hashlib.md5(htmlContent.encode()).hexdigest()
        driver.close()

        # detect duplicator by calculating seed canonical form
        # and check if seedCanonicalization has been already visited
        seedCanonicalization = parsed_uri.scheme + '://' + parsed_uri.netloc + parsed_uri.path

        # mark seed (that is now in proper form) as 'visited seed'
        if seedCanonicalization in visitedSeed:
            pageTypeCode = 'DUPLICATE'
        else:
            pageTypeCode = 'FRONTIER'
            visitedSeed.append(seedCanonicalization)

        # Duplicate po page content? Ker page url ima na nivoju baze nastavlen unique_url_index
        # sql = """select hash from crawldb.page where hash=%s;"""
        # cur.execute(sql, (htmlHash, ))
        # ce najde vsaj en record v tabeli, pomeni, da page ze obstaja -> duplicat
        # if cur.fetchone() is None:
        #    pageTypeCode = "FRONTIER"
        # else:
        #    pageTypeCode = "DUPLICATE"

        # insert into table | throws IntegrityError if url already exists
        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash) 
               VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        cur.execute(sql, (siteID(domain, conn), pageTypeCode, seed, htmlContent, response.status_code, datetime.datetime.now(), htmlHash))
        nextPageId = cur.fetchone()[0]
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (WebDriverException, TimeoutException) as error:
        print(error)
        return None
    except (Exception, psycopg2.IntegrityError) as error:
        print(error)
        return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()

    return nextPageId
