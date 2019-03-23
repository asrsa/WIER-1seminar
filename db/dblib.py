import threading
import psycopg2
import datetime

from psycopg2 import pool

__all__ = ["getSiteId", "insertPage", "insertLink",
           "getCanonUrl", 'getRobots', "updateFonrtierStatus",
           "insertBinary", "insertImage", "popFirstSeed", "insertSite",
           "closeConnectionPool", "getSiteId", "siteID"]

threadLock = threading.Lock()

# init connection pool
threaded_postgreSQL_pool = None
try:
    threaded_postgreSQL_pool = pool.ThreadedConnectionPool(3, 10,
                                                           user="postgres",
                                                           password="admin",
                                                           host="localhost",
                                                           port="5432",
                                                           database="crawldb")
    if threaded_postgreSQL_pool:
        print('Connection pool created successfully using ThreadedConnectionPool')
    else:
        print('Connection pool is None for some reason!')
        exit(1)
except Exception as error:
    print(error)


# DBLIB FUNCTIONS #


def closeConnectionPool():
    global threaded_postgreSQL_pool
    try:
        if threaded_postgreSQL_pool:
            threaded_postgreSQL_pool.closeall()
    except Exception as error:
        print(error)
    print('Threaded PostgreSQL connection pool is closed')


def updateFonrtierStatus(status, seedID):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        if status == 'BINARY':
            sql = """update crawldb.page set page_type_code=%s, html_content=%s where id=%s"""
            cur.execute(sql, ('BINARY', None, seedID))
        else:
            sql = """update crawldb.page set page_type_code=%s where id=%s"""
            cur.execute(sql, ('HTML', seedID))
        ps_connection.commit()
        threaded_postgreSQL_pool.putconn(ps_connection)

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        print(error)
        threaded_postgreSQL_pool.putconn(ps_connection)
        ps_connection.rollback()


def insertBinary(seedID, dataType, urlData):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        # obtaing data_type_code from binary file
        sql = """select code from crawldb.data_type where code like %s"""
        cur.execute(sql, (dataType.split('.')[1].upper(),))
        extension = cur.fetchone()
        if extension is not None:
            sql = """INSERT INTO crawldb.page_data(page_id, data_type_code, data)
                                VALUES (%s, %s, %s);"""
            cur.execute(sql, (seedID, extension, psycopg2.Binary(urlData.content)))
            ps_connection.commit()
        threaded_postgreSQL_pool.putconn(ps_connection)

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        print(error)
        threaded_postgreSQL_pool.putconn(ps_connection)
        ps_connection.rollback()


def insertImage(seedID, imageName, imageContentType, imageBytes):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time)
                             VALUES (%s,%s, %s, %s, %s);"""
        cur.execute(sql, (seedID, imageName, imageContentType, imageBytes.getvalue(), datetime.datetime.now()))
        ps_connection.commit()
        threaded_postgreSQL_pool.putconn(ps_connection)

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        print(error)
        threaded_postgreSQL_pool.putconn(ps_connection)
        ps_connection.rollback()


def popFirstSeed():
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        threadLock.acquire()
        cur = ps_connection.cursor()
        sql = """update crawldb.page set page_type_code=%s
                 where id=(select id from crawldb.page where page_type_code=%s LIMIT 1)
                 returning id, site_id, url, html_content"""
        cur.execute(sql, (None, 'FRONTIER'))
        ps_connection.commit()
        pageID = cur.fetchone()
        threadLock.release()
        threaded_postgreSQL_pool.putconn(ps_connection)
        return pageID

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threadLock.release()
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()


def getSiteId(domain):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
        cur.execute(sql, (domain,))
        data = cur.fetchone()
        cur.close()
        threaded_postgreSQL_pool.putconn(ps_connection)
        return data

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()


def insertPage(site, pageTypeCode, seed, htmlContent, status_code, datetime, htmlHash, seedCanonicalization):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """INSERT INTO crawldb.page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash, canon_url) 
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        cur.execute(sql, (site, pageTypeCode, seed, htmlContent, status_code, datetime, htmlHash, seedCanonicalization))
        nextPageId = cur.fetchone()[0]
        ps_connection.commit()
        cur.close()
        threaded_postgreSQL_pool.putconn(ps_connection)
        return nextPageId

    except (Exception, psycopg2.IntegrityError, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        #print(error)
        ps_connection.rollback()
        return None


def insertLink(link1, link2):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """INSERT INTO crawldb.link(from_page, to_page) 
                            VALUES(%s, %s);"""
        cur.execute(sql, (link1, link2))
        ps_connection.commit()
        threaded_postgreSQL_pool.putconn(ps_connection)

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()


def getCanonUrl(url):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """SELECT id FROM crawldb.page WHERE canon_url=%s"""
        cur.execute(sql, (url,))
        data = cur.fetchone()
        cur.close()
        threaded_postgreSQL_pool.putconn(ps_connection)
        return data

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()


def getRobots(siteId):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """SELECT robots_content FROM crawldb.site WHERE id=%s"""
        cur.execute(sql, (siteId,))
        data = cur.fetchone()[0]
        cur.close()
        threaded_postgreSQL_pool.putconn(ps_connection)
        return data

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()


def insertSite(domain, robots, sitemap):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """INSERT INTO crawldb.site(domain, robots_content, sitemap_content) 
                    SELECT %s, %s, %s
                    WHERE NOT EXISTS (
                    SELECT 1 FROM crawldb.site WHERE domain=%s
                );"""
        cur.execute(sql, (domain, robots, sitemap, domain))
        ps_connection.commit()
        threaded_postgreSQL_pool.putconn(ps_connection)

    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()


def siteID(domain):
    try:
        ps_connection = threaded_postgreSQL_pool.getconn()
        cur = ps_connection.cursor()
        sql = """SELECT id FROM crawldb.site WHERE domain=%s"""
        cur.execute(sql, (domain, ))
        id = cur.fetchone()[0]
        threaded_postgreSQL_pool.putconn(ps_connection)
        return id
    except (Exception, psycopg2.DatabaseError, pool.PoolError) as error:
        threaded_postgreSQL_pool.putconn(ps_connection)
        print(error)
        ps_connection.rollback()
