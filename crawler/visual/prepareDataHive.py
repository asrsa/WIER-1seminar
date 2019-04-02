import psycopg2
import json

from db.config import config


conn = None


# database code
try:
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    data = []


    # fetch all
    print('\n')
    cur.execute("SELECT * FROM crawldb.page")
    rows = cur.fetchall()
    for row in rows:
        print(str(row[3]) + " -- " + str(row[1]) + " -- " + str(row[0]))
        tmp = {}
        tmp['name'] = str(row[0])
        tmp['size'] = row[1]
        tmp['url'] = str(row[8])

        cur.execute("SELECT * FROM crawldb.link \n" +
                    "WHERE from_page = %s", (row[0],))
        links = cur.fetchall()

        tmplinks = []
        for link in links:
            print(link)

            if link[1] != row[0]:
                tmplinks.append(link[1])

        tmp['imports'] = tmplinks

        data.append(tmp)


    # close the communication with the PostgreSQL
    cur.close()

    with open('dataHive.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')

