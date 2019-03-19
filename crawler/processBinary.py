import psycopg2
import requests
from db.config import config

includeBinary = ['.pdf', '.doc', '.ppt', '.docx', '.pptx']


def processBinaryData(seed, seedID, conn):

    # check if binary data is stored or not
    print('inside binary data')
    for dataType in includeBinary:
        if dataType in seed:
            urlData = requests.get(seed)

            # conn = None
            try:
                # params = config()
                # conn = psycopg2.connect(**params)

                # create a cursor
                cur = conn.cursor()

                # obtaing data_type_code from binary file
                sql = """select code from crawldb.data_type where code like %s"""
                cur.execute(sql, (dataType.split('.')[1].upper(), ))
                extension = cur.fetchone()
                if extension is None:
                    # extension not recognized -> raise error?
                    print("error")

                sql = """INSERT INTO crawldb.page_data(page_id, data_type_code, data)
                                    VALUES (%s, %s, %s);"""
                cur.execute(sql, (seedID, extension, psycopg2.Binary(urlData.content)))
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                conn.rollback()
            # finally:
            #    if conn is not None:
            #        conn.close()
