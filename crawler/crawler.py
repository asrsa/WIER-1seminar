from urllib.parse import urlparse
from processFrontier import processFrontier
from bs4 import BeautifulSoup
from processBinary import processBinaryData
from processImg import processImg
from db.dblib import *


def processSeed(option, domains, page):
    try:
        if page[3] is None:
            # update record in DB
            updateFonrtierStatus('BINARY', page[0])

            # call function to process binary data type
            processBinaryData(page[2], page[0])
        else:
            # update record in DB
            updateFonrtierStatus('HTML', page[0])

            # beautify html content
            rawHtml = BeautifulSoup(str(page[3]), 'html.parser')

            for imageObject in rawHtml.find_all('img'):
                imageSrc = str(imageObject.get('src'))

                if 'http' not in imageSrc:
                    urlParts = urlparse(page[2])
                    imageSrc = urlParts.scheme + '://' + urlParts.netloc + imageSrc
                processImg(imageSrc, page[0])

            for link in rawHtml.find_all('a', href=True):
                url = str(link.get('href'))

                # transform /si -> https://e-uprava.gov.si/si
                if 'http' not in url:
                    urlParts = urlparse(page[2])
                    if not url.startswith('/') and not url.startswith('#'):
                        url = urlParts.scheme + '://' + urlParts.netloc + '/' + url
                    else:
                        url = urlParts.scheme + '://' + urlParts.netloc + url

                # add url to frontier
                nextPageId = processFrontier(url, option, domains)
                currPageId = page[0]

                if nextPageId is not None:
                    insertLink(currPageId, nextPageId)
                else:
                    insertLink(currPageId, currPageId)
    except Exception as error:
        print(error)
