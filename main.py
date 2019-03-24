import os
import threading
from crawler import processSeed
from db import dblib
from db.dblib import popFirstSeed, closeConnectionPool
from processFrontier import processFrontier

seedPages = ['http://e-uprava.gov.si', 'http://www.evem.gov.si',
             'http://podatki.gov.si', 'http://e-prostor.gov.si']
seedPages = ['http://e-prostor.gov.si']

# option: 0 - within given site domain (save img / binary)
#         1 - within .gov.si domain (don't save img / binary)
option = 0
domains = seedPages
threadsNumber = 4
threads = []


# thread class - stores thread ID and conn object that thread uses to communicate with DB
class customThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        seedQueueHasSeeds = True
        while seedQueueHasSeeds:
            page = popFirstSeed()
            if page is not None:
                print(page[0], end=' | ')
                print(self.threadID)
                processSeed(option, domains, page)
            else:
                seedQueueHasSeeds = False

        # when thread is done, put back conn object
        print('thread finished')


# init media folder
if not os.path.exists('media'):
    os.mkdir('media')

# start crawling
if dblib.threaded_postgreSQL_pool:
    for seed in seedPages:
        processFrontier(seed, option, domains)
    print('Init frontier done!')

    # create threads
    for i in range(threadsNumber):
        t = customThread(i)
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print('All seeds have been processed!')
    closeConnectionPool()
else:
    print('Connection pool error! Quiting program ...')
