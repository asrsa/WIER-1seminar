import os
import threading
import psycopg2
from psycopg2 import pool
from crawler import processSeed
from db.dblib import popFirstSeed
from processFrontier import processFrontier

seedPages = ['http://e-uprava.gov.si', 'http://www.evem.gov.si',
                'http://podatki.gov.si', 'http://e-prostor.gov.si']
seedPages = ['http://e-uprava.gov.si']

# option: 0 - within given site domain (save img / binary)
#         1 - within .gov.si domain (don't save img / binary)
option = 0
domains = seedPages
threadsNumber = 4

threaded_postgreSQL_pool = None
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
            page = popFirstSeed(self.conn)
            if page is not None:
                print(page[0], end=' | ')
                print(self.threadID)
                processSeed(option, domains, self.conn, page)

            else:
                seedQueueHasSeeds = False

        # when thread is done, put back conn object
        print('thread finished')
        threaded_postgreSQL_pool.putconn(ps_connection)


try:
    # init media folder
    if not os.path.exists('media'):
        os.mkdir('media')

    threaded_postgreSQL_pool = pool.ThreadedConnectionPool(3, 10,
                                                           user="postgres",
                                                           password="admin",
                                                           host="localhost",
                                                           port="5432",
                                                           database="crawldb")
    if threaded_postgreSQL_pool:
        print('Connection pool created successfully using ThreadedConnectionPool')

    ps_connection = threaded_postgreSQL_pool.getconn()
    for seed in seedPages:
        processFrontier(seed, option, domains, ps_connection)
    print('Init frontier done!')
    threaded_postgreSQL_pool.putconn(ps_connection)
    # create threads
    for i in range(threadsNumber):
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
