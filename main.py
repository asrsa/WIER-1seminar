import psycopg2
import processFrontier
from crawler import processSeed
from db.config import config

seedPagesTmp = ['https://e-uprava.gov.si', 'http://evem.gov.si',
             'https://podatki.gov.si', 'http://e-prostor.gov.si']
seedPages = ['https://e-uprava.gov.si']
conn = None

# init domainList ['gov.si', etc.]
includeBinary = ['.pdf', '.doc', '.ppt', '.jpg', '.png']

# init frontier
for seed in seedPages:
    processFrontier.processFrontier(seed)
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

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
print('All seeds have been processed!')
