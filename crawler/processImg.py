import io
import os
import urllib
import wget as wget
from PIL import Image
import requests
from db.dblib import insertImage


def processImg(seed, seedID, conn):
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

        # insert image into DB
        insertImage(conn,seedID, imageName, imageContentType, imageBytes)

        # download image
        if not os.path.exists('media\\' + str(seedID)):
            os.mkdir('media\\' + str(seedID))

        wget.download(seed, out=str('media\\' + str(seedID) + '\\'))

    except (Exception, IOError) as error:
        print(error)
