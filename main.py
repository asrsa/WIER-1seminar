import processFrontier

# init domainList ['gov.si', etc.]
# media ['.pdf', etc.]

seedPagesTmp = ['https://e-uprava.gov.si', 'http://evem.gov.si',
             'https://podatki.gov.si', 'http://e-prostor.gov.si']

seedPages = ['https://e-uprava.gov.si']

for seed in seedPages:
    processFrontier.processFrontier(seed)
