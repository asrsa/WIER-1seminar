import os
import requests
import wget
from db.dblib import insertBinary

includeBinary = ['.pdf', '.doc', '.ppt', '.docx', '.pptx']


def processBinaryData(seed, seedID, option):

    # check if binary data is stored or not
    for dataType in includeBinary:
        if dataType in seed:
            urlData = requests.get(seed)
            try:
                # save binary into DB
                if option == 1:
                    urlData = None
                insertBinary(seedID, dataType, urlData)

                # dowload file
                if option == 0:
                    if not os.path.exists('media\\' + str(seedID)):
                        os.mkdir('media\\' + str(seedID))
                    wget.download(seed, out=str('media\\' + str(seedID) + '\\'))

            except Exception as error:
                print(error)
