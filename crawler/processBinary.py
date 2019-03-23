import os
import requests
import wget
from db.dblib import insertBinary

includeBinary = ['.pdf', '.doc', '.ppt', '.docx', '.pptx']


def processBinaryData(seed, seedID):

    # check if binary data is stored or not
    print('inside binary data')
    for dataType in includeBinary:
        if dataType in seed:
            urlData = requests.get(seed)
            try:
                # save binary into DB
                insertBinary(seedID, dataType, urlData)

                # dowload file
                if not os.path.exists('media\\' + str(seedID)):
                    os.mkdir('media\\' + str(seedID))
                wget.download(seed, out=str('media\\' + str(seedID) + '\\'))

            except Exception as error:
                print(error)
