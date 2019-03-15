# TODO: reimplement from code below; instead readin binary image from physical file located on disk, read from URL

# seed -> current page URL
# seedID -> current pageID
# filename -> obtain from url?
# content_type -> obtain from ???
# accessed_date -> datetime.datetime.now()

# def processImg(seed, pageID):
  # myPic = read image object from given URL
  # mypic=open('c:/sun.jpg','rb').read()
  # ursor = conn.cursor()
  # sql = """INSERT INTO crawldb.image(pageID, filename, content_type, data, accessed_date)
  #                        VALUES (%s,%s, %s, %s, %s);"""
  # cursor.execute(sql, (pageID, Image_name, psycopg2.Binary(imgObject)), datetime.datetime.now())
  # conn.commit()
