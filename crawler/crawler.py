import psycopg2
from processFrontier import processFrontier
from bs4 import BeautifulSoup
from db.config import config
from processBinary import processBinaryData
from processImg import processImg

from db.dblib import *

# TODO crawler implementation
#   get frontier, set:
#                 HTML  če je htmlContetn not null -> init frontier
#                 BINARY ce je null -> download binary and insert int sql
#   FOREACH LNKS <a>
#       link in domainList  [opt: binary in media list]
#       add page to frontier: returning ID  (call init_frontier(url))
#       add Links from page - to page (currPageId -> returning id page)


def processSeed():
    # get first seed from frontier
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        sql = """select id, site_id, url, html_content, hash, id from crawldb.page where page_type_code=%s"""
        cur.execute(sql, ('FRONTIER', ))
        seedData = cur.fetchone()

        sql = """select domain from crawldb.site where id=%s"""
        cur.execute(sql, (seedData[1], ))
        seedDomain = cur.fetchone()
        if seedDomain is not None:
            seedDomain = 'https://' + seedDomain[0]
        # print(seedDomain)

        # TODO check HTML content
        if seedData[3] is None:
            # binary data
            sql = """update crawldb.page set page_type_code=%s, html_content=%s where site_id=%s"""
            cur.execute(sql, ('BINARY', None, seedData[1]))
            conn.commit()

            # call function to process binary data type
            processBinaryData(seedData[2], seedData[0])
        else:
            # html data
            sql = """update crawldb.page set page_type_code=%s where site_id=%s"""
            cur.execute(sql, ('HTML', seedData[1]))
            conn.commit()

            # beautify html content
            rawHtml = BeautifulSoup(str(seedData[3]), 'html.parser')

            # find images first, otherwise cralwer will process fist all the links in the forntier
            # -> images will come at end (might never be extracted at all)

            # extract images from rawHtml | seedData[0] is current_page_id
            # let's assume there is FULL image URL in img tag
            for imageObject in rawHtml.find_all('img'):
                imageSrc = str(imageObject.get('src'))
                # print(imageSrc)
                # process image using processImg function
                processImg(imageSrc, seedData[0], seedDomain)

            # should there be single foor loop with 2 conditions
            # for <a href> and <img>?
            # extract links <a href ... >
            for link in rawHtml.find_all('a'):
                # print(link.get('href'))
                url = str(link.get('href'))

                # transform /si -> https://e-uprava.gov.si/si
                if 'http' not in url:
                    url = str(seedData[2]) + url
                # print(url)

                # add url to frontier
                nextPageId = processFrontier(url)
                currPageId = seedData[5]

                if nextPageId is not None:
                    insertLink(currPageId, nextPageId)
                else:
                    insertLink(currPageId, currPageId)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
