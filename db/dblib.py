import psycopg2
import datetime
from db.config import config

__all__ = ["getFrontier", "getSiteId", "insertPage", "insertLink",
           "getPageId", 'getCanonUrl', 'getRobots']

def getFrontier(conn):
    # conn = None
    try:
    #    params = config()
    #    conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.page WHERE page_type_code='FRONTIER'"""

        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()

def getSiteId(domain, conn):
    # conn = None
    try:
    #    params = config()
    #    conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
        cur.execute(sql, (domain,))
        data = cur.fetchone()
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    #finally:
    #    if conn is not None:
    #        conn.close()

def getPageId(url, conn):
    # conn = None
    try:
    #    params = config()
    #    conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.page WHERE url=%s"""
        cur.execute(sql, (url,))
        data = cur.fetchone()[0]
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()

def insertPage(pageData, conn):
    #conn = None
    try:
    #    params = config()
    #    conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time) 
                        VALUES(%s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (getSiteId(pageData[0]), pageData[1], pageData[2], pageData[3], pageData[4], datetime.datetime.now()))
        conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()

def insertLink(link1, link2, conn):
    try:
        # params = config()
        # conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """INSERT INTO crawldb.link(from_page, to_page) 
                            VALUES(%s, %s);"""
        cur.execute(sql, (link1, link2))
        conn.commit()

        # cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        #print(error)
        # ce faila, naj bo rollback(), cene se use pokvar :s
        conn.rollback()
    # finally:
    #    if conn is not None:
    #        conn.close()


def getCanonUrl(url, conn):
    # conn = None
    try:
        # params = config()
        # conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.page WHERE canon_url=%s"""

        cur.execute(sql, (url,))
        data = cur.fetchone()
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()

def getRobots(siteId, conn):
    #conn = None
    try:
    #    params = config()
    #    conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT robots_content FROM crawldb.site WHERE id=%s"""
        cur.execute(sql, (siteId,))
        data = cur.fetchone()[0]
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()