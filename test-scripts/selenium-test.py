import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'), options=options)
driver.get("http://fri.uni-lj.si")

for n in driver.find_elements_by_class_name('news-container-title'):
    if len(n.text) > 0:
        print(n.text)

driver.close()