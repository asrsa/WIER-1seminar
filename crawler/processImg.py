import io
import psycopg2
from PIL import Image
from db.config import config
import requests
import datetime

# seed -> current page URL
# seedID -> current pageID
# data -> retrieved image from url and converted to bytea type and stored into DB
# TODO implement function or method to calculate image_name from url?
# filename ->
# TODO content_type? Wtf would that be?
# content_type ->
# accessed_date ->datetime.datetime.now()


def processImg(seed, seedID, domain):
    conn = None
    # read image object from given URL
    try:
        # TODO: fix seed urls? or just skip?
        # /.imaging/stk/euprava/medium/dam/eUprava2-multimedia/Slike-razno/Kazenske-tocke/jcr:content/Kazenske%20tocke.png.2019-03-13-14-56-26.png
        # should be https://e-uprava.gov.si/.imaging/stk/euprava/medium/dam/eUprava2-multimedia/Slike-razno/Kazenske-tocke/jcr:content/Kazenske%20tocke.png.2019-03-13-14-56-26.png
        if 'http' not in seed:
            seed = str(domain) + str(seed)

        # imageObject = Image.open(requests.get(seed, stream=True).raw)
        imageRequest = requests.get(seed, stream=True).raw
        imageObject = Image.open(imageRequest)
        # print(imageObject)    # prints <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=775x518 at 0x4B19FD0>

        # convert imageObject [PIL.JpegImagePlugin.JpegImageFile] to binary array
        # colum data in postgres is type of bytea
        imageBytes = io.BytesIO()
        # TODO resolve format!
        if '.jpeg' in seed or '.jpg' in seed:
            imageObject.save(imageBytes, format='JPEG')
        elif '.png' in seed:
            imageObject.save(imageBytes, format='PNG')
        else:
            imageObject.save(imageBytes)
        # print(imageBytes)                          # prints <_io.BytesIO object at 0x04B83090>
        # print(imageBytes.getvalue())               # prints b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01...

        params = config()
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
      
        sql = """INSERT INTO crawldb.image(page_id, filename, content_type, data, accessed_time)
                             VALUES (%s,%s, %s, %s, %s);"""
        cur.execute(sql, (seedID, seed, 'content', imageBytes.getvalue(), datetime.datetime.now()))
        conn.commit()

    except (Exception, IOError) as error:
        print(error)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
