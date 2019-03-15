# TODO: reimplement from code below; instead readin binary image from physical file located on disk, read from URL
import psycopg2
from PIL import Image
from db.config import config
import requests
import datetime

# seed -> current page URL
# seedID -> current pageID
# TODO implement function or method to calculate image_name from url?
# filename -> 
# content_type -> obtained from ???
# accessed_date -> datetime.datetime.now()

def processImg(seed, pageID):
  # read image object from given URL
  imageObject = Image.open(requests.get(seed, stream=True).raw)
  conn = None
  try:
      params = config()
      conn = psycopg2.connect(**params)
      
      # create a cursor
      cur = conn.cursor()
      
      sql = """INSERT INTO crawldb.image(pageID, filename, content_type, data, accessed_date)
                            VALUES (%s,%s, %s, %s, %s);"""
      cur.execute(sql, (pageID, Image_name, psycopg2.Binary(imgObject)), datetime.datetime.now())
      conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
      print(error)
  finally:
      if conn is not None:
          conn.close()
