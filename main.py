import time

import psycopg2
from crawler import processSeed
from db.config import config
from processFrontier import processFrontier

seedPagesTmp = ['https://e-uprava.gov.si', 'http://evem.gov.si',
                'https://podatki.gov.si', 'http://e-prostor.gov.si']
seedPages = ['https://e-uprava.gov.si']

# test for images extraction. Use thi url to obtain background image from airbnb site.
# uncomment and run this to test saving images into DB. There are 3 images stored into DB.
# also make sure that code that is extracting <a href> in comment. Only process home page
# seedPages = ['https://www.airbnb.com/']

# test - pdf extraction. Read binary object and store it into DB
# seedPages = ['http://www.africau.edu/images/default/sample.pdf']

conn = None

# init frontier
for seed in seedPages:
    processFrontier(seed)
print('Init frontier done!')

seedQueueHasSeeds = True
while seedQueueHasSeeds:
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """select page_type_code from crawldb.page where page_type_code=%s"""
        cur.execute(sql, ('FRONTIER', ))
        if cur.fetchone() is None:
            # no more FRONTIER seeds -> seedQueue si empty
            seedQueueHasSeeds = False
        else:
            # 'poll' first seed and process it
            processSeed()
        time.sleep(1)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
print('All seeds have been processed!')
