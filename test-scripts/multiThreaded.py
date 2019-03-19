import threading
import time
import psycopg2
from psycopg2 import pool
from crawler import processSeed
from db.config import config

seedPages = ['https://podatki.gov.si']

threaded_postgreSQL_pool = None

# option: 0 - within given site domain (save img / binary)
#         1 - within .gov.si domain (don't save img / binary)
option = 0
domains = seedPages

threadLock = threading.Lock()
threads = []


# thread class - stores thread ID and conn object that thread uses to communicate with DB
class customThread(threading.Thread):
    def __init__(self, threadID, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn

    def run(self):
        seedQueueHasSeeds = True
        while seedQueueHasSeeds:
            threadLock.acquire()
            cur = self.conn.cursor()

            # perform update just for one row and with RETURNING ID?

            sql = """select id, page_type_code from crawldb.page where page_type_code=%s"""
            cur.execute(sql, ('FRONTIER',))
            # pageID must be passed to processSeed function!
            # also conn object should be passing to all function too - thread has his own conn object from conn pool!
            # Or conn object is put back to pool after every sql statement
            # and retrieved again before every sql statement - need to have 'global' reference to conn pol then
            # Also add seedData to function
            # to sum all up -> processSeed(option, domains, seedData, conn)
            seedData = cur.fetchone()
            if seedData is not None:
                print(seedData[0], end=' | ')
                print(self.threadID)
                # update site_id to duplicate so the other thread wont select the same page
                sql = """update crawldb.page set page_type_code=%s, html_content=%s where id=%s"""
                cur.execute(sql, (None, None, seedData[0]))
                self.conn.commit()
                threadLock.release()
                time.sleep(1)
            else:
                seedQueueHasSeeds = False

                # if cur.fetchone() is None:
                #    # no more FRONTIER seeds -> seedQueue si empty
                #    seedQueueHasSeeds = False
                # else:
                #    # 'poll' first seed and process it
                #    processSeed(option, domains)

        # when thread is done, put back conn object
        threaded_postgreSQL_pool.putconn(ps_connection)


try:
    threaded_postgreSQL_pool = pool.ThreadedConnectionPool(1, 5,
                                                           user="postgres",
                                                           password="admin",
                                                           host="localhost",
                                                           port="5432",
                                                           database="crawldb")
    if threaded_postgreSQL_pool:
        print('Connection pool created successfully using ThreadedConnectionPool')

    # create threads
    for i in range(2):
        ps_connection = threaded_postgreSQL_pool.getconn()
        if ps_connection:
            print('successfully received connection from connection pool')
            ps_connection = threaded_postgreSQL_pool.getconn()
            t = customThread(i, ps_connection)
            t.start()
            threads.append(t)


    # Wait for all threads to complete
    for t in threads:
        t.join()


except (Exception, psycopg2.DatabaseError) as error:
    print('Error while connecting to PostgreSQL', error)

finally:
    # closing database connection.
    # use closeall method to close all the active connection if you want to turn of the application
    if threaded_postgreSQL_pool:
        threaded_postgreSQL_pool.closeall()
    print('Threaded PostgreSQL connection pool is closed')
print('All seeds have been processed!')