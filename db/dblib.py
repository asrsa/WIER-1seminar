import psycopg2
import datetime
from db.config import config

__all__ = ["getFrontier", "getSiteId", "insertPage", "insertLink",
           "getPageId"]

def getFrontier():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.page WHERE page_type_code='FRONTIER'"""

        cur.execute(sql)
        return cur.fetchall()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getSiteId(domain):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
        cur.execute(sql, (domain,))
        return cur.fetchone()[0]

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getPageId(url):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """SELECT id FROM crawldb.page WHERE url=%s"""
        cur.execute(sql, (url,))
        return cur.fetchone()[0]

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertPage(pageData):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time) 
                        VALUES(%s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (getSiteId(pageData[0]), pageData[1], pageData[2], pageData[3], pageData[4], datetime.datetime.now()))
        conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertLink(link1, link2):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """INSERT INTO crawldb.link(from_page, to_page) 
                            VALUES(%s, %s);"""
        cur.execute(sql, (link1, link2))
        conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

