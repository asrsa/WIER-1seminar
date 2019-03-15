import psycopg2
from processFrontier import processFrontier
from bs4 import BeautifulSoup
from db.config import config
from processBinary import processBinaryData
from processImg import processImg

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
        sql = """select site_id, url, html_content, hash from crawldb.page where page_type_code=%s"""
        cur.execute(sql, ('FRONTIER', ))
        seedData = cur.fetchone()

        # TODO check HTML content
        if seedData[2] is None:
            # binar data
            sql = """update crawldb.page set page_type_code=%s, html_content=%s where site_id=%s"""
            cur.execute(sql, ('BINARY', None, seedData[0]))
            conn.commit()

            # call funtion to process binary data type
            processBinaryData()
        else:
            # html data
            sql = """update crawldb.page set page_type_code=%s where site_id=%s"""
            cur.execute(sql, ('HTML', seedData[0]))
            conn.commit()

            # beautify html content
            rawHtml = BeautifulSoup(str(seedData[2]), 'html.parser')

            # should there be single foor loop with 2 conditions
            # for <a href> and <img>?
            # extract links <a href ... >
            for link in rawHtml.find_all('a'):
                # print(link.get('href'))
                url = str(link.get('href'))

                # transform /si -> https://e-uprava.gov.si/si
                if 'http' not in url:
                    url = str(seedData[1]) + url
                # print(url)

                # add url to frontier
                processFrontier(url)
                
            # extract images from rawHtml
            # let's assume there is FULL image URL in img tag
            # seedData[0] is current_page_id
            for imageSrc in rawHtml.find_all('img')
                # process image using processImg function
                processImg(imageScr, seedData[0])
            

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
