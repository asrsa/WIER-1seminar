import threading
import psycopg2
import datetime

__all__ = ["getFrontier", "getSiteId", "insertPage", "insertLink",
           "getPageId", 'getCanonUrl', 'getRobots', "updateFonrtierStatus",
           "insertBinary", "insertImage", "popFirstSeed", "insertSite"]

threaded_postgreSQL_pool = None
threadLock = threading.Lock()


def updateFonrtierStatus(conn, status, seedID):
    try:
        cur = conn.cursor()
        if status == 'BINARY':
            sql = """update crawldb.page set page_type_code=%s, html_content=%s where id=%s"""
            cur.execute(sql, ('BINARY', None, seedID))
        else:
            sql = """update crawldb.page set page_type_code=%s where id=%s"""
            cur.execute(sql, ('HTML', seedID))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()


def insertBinary(conn, seedID, dataType, urlData):
    try:
        cur = conn.cursor()
        # obtaing data_type_code from binary file
        sql = """select code from crawldb.data_type where code like %s"""
        cur.execute(sql, (dataType.split('.')[1].upper(),))
        extension = cur.fetchone()
        if extension is not None:
            sql = """INSERT INTO crawldb.page_data(page_id, data_type_code, data)
                                VALUES (%s, %s, %s);"""
            cur.execute(sql, (seedID, extension, psycopg2.Binary(urlData.content)))
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()


def insertImage(conn, seedID, imageName, imageContentType, imageBytes):
    try:
        cur = conn.cursor()
        sql = """INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time)
                             VALUES (%s,%s, %s, %s, %s);"""
        cur.execute(sql, (seedID, imageName, imageContentType, imageBytes.getvalue(), datetime.datetime.now()))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()


def popFirstSeed(conn):
    try:
        threadLock.acquire()
        cur = conn.cursor()
        sql = """update crawldb.page set page_type_code=%s
                 where id=(select id from crawldb.page where page_type_code=%s LIMIT 1)
                 returning id, site_id, url, html_content"""
        cur.execute(sql, (None, 'FRONTIER'))
        conn.commit()
        pageID = cur.fetchone()
        threadLock.release()
        return pageID

    except (Exception, psycopg2.DatabaseError) as error:
        threadLock.release()
        print(error)
        conn.rollback()


def getFrontier(conn):
    try:
        cur = conn.cursor()
        sql = """SELECT id FROM crawldb.page WHERE page_type_code='FRONTIER'"""
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getSiteId(domain, conn):
    try:
        cur = conn.cursor()
        sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
        cur.execute(sql, (domain,))
        data = cur.fetchone()
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getPageId(url, conn):
    try:
        cur = conn.cursor()
        sql = """SELECT id FROM crawldb.page WHERE url=%s"""
        cur.execute(sql, (url,))
        data = cur.fetchone()[0]
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insertPage(conn, site, pageTypeCode, seed, htmlContent, status_code, datetime, htmlHash, seedCanonicalization):
    try:
        cur = conn.cursor()
        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash, canon_url) 
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        cur.execute(sql, (site, pageTypeCode, seed, htmlContent, status_code, datetime, htmlHash, seedCanonicalization))
        nextPageId = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return nextPageId

    except (Exception, psycopg2.IntegrityError, psycopg2.DatabaseError) as error:
        #print(error)
        conn.rollback()
        return None


def insertLink(link1, link2, conn):
    try:
        cur = conn.cursor()
        sql = """INSERT INTO crawldb.link(from_page, to_page) 
                            VALUES(%s, %s);"""
        cur.execute(sql, (link1, link2))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()


def getCanonUrl(url, conn):
    try:
        cur = conn.cursor()
        sql = """SELECT id FROM crawldb.page WHERE canon_url=%s"""
        cur.execute(sql, (url,))
        data = cur.fetchone()
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getRobots(siteId, conn):
    try:
        cur = conn.cursor()
        sql = """SELECT robots_content FROM crawldb.site WHERE id=%s"""
        cur.execute(sql, (siteId,))
        data = cur.fetchone()[0]
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insertSite(conn, domain, robots, sitemap):
    try:
        cur = conn.cursor()
        sql = """INSERT INTO crawldb.site(domain, robots_content, sitemap_content) 
                    SELECT %s, %s, %s
                    WHERE NOT EXISTS (
                    SELECT 1 FROM crawldb.site WHERE domain=%s
                );"""
        cur.execute(sql, (domain, robots, sitemap, domain))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
