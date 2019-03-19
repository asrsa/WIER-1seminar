import io
import urllib

import psycopg2
from PIL import Image
from db.config import config
import requests
import datetime


def processImg(seed, seedID, conn):
    # conn = None
    try:
        # calculate image_name
        urlParts = urllib.parse.urlparse(seed)
        imageName = urlParts[2].rpartition('/')[2]

        # content type
        imageContentType = 'unknown'

        # imageObject = Image.open(requests.get(seed, stream=True).raw)
        imageRequest = requests.get(seed, stream=True).raw
        imageObject = Image.open(imageRequest)
        # print(imageObject)    # prints <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=775x518 at 0x4B19FD0>

        # convert imageObject [PIL.JpegImagePlugin.JpegImageFile] to binary array
        # colum data in postgres is type of bytea
        imageBytes = io.BytesIO()

        if '.jpeg' in seed or '.jpg' in seed:
            imageObject.save(imageBytes, format='JPEG')
            imageContentType = 'JPEG' if '.jpeg' in seed else 'JPG'
        elif '.png' in seed:
            imageObject.save(imageBytes, format='PNG')
            imageContentType = 'PNG'
        else:
            imageObject.save(imageBytes)
        # print(imageBytes)                          # prints <_io.BytesIO object at 0x04B83090>
        # print(imageBytes.getvalue())               # prints b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01...

    #    params = config()
    #    conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
      
        sql = """INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time)
                             VALUES (%s,%s, %s, %s, %s);"""
        cur.execute(sql, (seedID, imageName, imageContentType, imageBytes.getvalue(), datetime.datetime.now()))
        conn.commit()

    except (Exception, IOError) as error:
        print(error)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    #finally:
    #    if conn is not None:
    #        conn.close()
