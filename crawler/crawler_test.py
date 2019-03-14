from db.dblib import *


# print('Frontier(site id): ' + str(getFrontier()[0][0]))
# print('Site id(by domain): ' + str(getSiteId('podatki.gov.si')))
print('Page id(by url): ' + str(getPageId('https://e-uprava.gov.si')))

pageData = ['podatki.gov.si', 'FRONTIER', 'podatki.gov.si/test/page', '<html></html>', 200]

#insertPage(pageData)
#insertLink(14, 15)