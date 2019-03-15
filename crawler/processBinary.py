from db.config import config


# TODO: implementacija funkcije, ki obdela seed tipa BINARY
def processBinaryData(seed, seedID):
    print('Not yet implemented')
    
    # store binary data into 
    # store url instead of binary data of file for now
    # binaryObject = requests.get(seed, stream=True).raw
    binaryObject = seed
    
    # name of binary object obtained from url? with extension
    binaryObjectName = 'something.pdf'
    
    conn = None
    try:
      params = config()
      conn = psycopg2.connect(**params)

      # create a cursor
      cur = conn.cursor()
        
      # obtaing data_type_code from binary file
      sql = """select code from crawldb.data_type where code like %s"""
      cur.execute(sl, (binaryObject.split('.')[1].upper(), ))
      extension = cur.fetchone()
      if extension is None:
        # extension not recognized -> raise error?
      
        
      sql = """INSERT INTO crawldb.page_data(pageID, data_type_code, data)
                            VALUES (%s, %s, %s);"""
      cur.execute(sql, (seedID, extension, psycopg2.Binary(binaryObject)))
      conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
          conn.close()
