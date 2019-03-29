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

    data = {}
    data['nodes'] = []
    data['links'] = []

    # fetch all
    print('\n')
    cur.execute("SELECT * FROM crawldb.page \n" +
                "WHERE page_type_code = 'HTML'")
    rows = cur.fetchall()
    for row in rows:
        print(str(row[3]) + " -- " + str(row[1]) + " -- " + str(row[0]))

        data['nodes'].append({
            'id': str(row[3]),
            'group': str(row[1])
        })


        cur.execute("SELECT * FROM crawldb.link \n" +
                    "WHERE from_page = %s", (row[0],))
        links = cur.fetchall()
        for link in links:
            print(link)
            data['links'].append({
                'source': link[0],
                'target': link[1],
                'value': 1
            })

    # close the communication with the PostgreSQL
    cur.close()

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')

