import hashlib
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from db.dblib import *
from urllib.parse import urlparse
import requests
import datetime
import urllib.robotparser
import time
import xml.etree.ElementTree as ET

userAgent = "Chrome/73.0.3683.75 Safari/537.36"


def getSitemap(robots):
    for line in robots.splitlines():
        if "sitemap" in line:
            smap = requests.get(line.split(' ')[1])
            return smap.text


def processSitemap(option, domains, sitemap):
    root = ET.fromstring(sitemap)
    print("Started Sitemap")
    for url in root:
        # print(url[0].text)
        processFrontier(url[0].text, option, domains)
    print("Finished sitemap")


def processFrontier(seed, option, domains):
    # Remove 'www.' from seeds
    seed = seed.replace('www.', '')
    print('Processing ' + seed)

    parsed_uri = urlparse(seed)
    domain = '{uri.netloc}'.format(uri=parsed_uri)

    if option == 0 and not any(domain in d for d in domains):
        # print("not in site domain, skipping")
        return

    if option == 1 and not domains[0] in seed:
        # print("not in site domain, skipping")
        return

    chrome_options = Options()
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(20)                        # wait 20 seconds, move to next url after timeout

    # wait 3 secs for web to load
    driver.implicitly_wait(3)

    nextPageId = None
    try:
        robots = None
        sitemap = None

        response = requests.get(seed)
        parsed_uri = urlparse(seed)
        domain = '{uri.netloc}'.format(uri=parsed_uri)

        if getSiteId(domain) is None:
            responseRobots = requests.get(parsed_uri[0] + '://' + domain + '/robots.txt')
            if responseRobots.status_code == 200:
                robots = responseRobots.text
                sitemap = getSitemap(robots)

            # to avoid 'A string literal cannot contain NUL (0x00) characters' exception from postgresql IntegrityError
            # replace all '\x00' characters to '' (blank) in robots and site variable
            if robots is not None:
                robots = robots.replace('\x00', '')
            if sitemap is not None:
                sitemap = sitemap.replace('\x00', '')

            insertSite(domain, robots, sitemap)

            if sitemap is not None:
                # PROCESS SITEMAP
                processSitemap(option, domains, sitemap)

        # ROBOTS CHECK
        site = siteID(domain)
        robots_content = getRobots(site)

        if robots_content is not None:
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(robots_content.splitlines())

            if not rp.can_fetch(userAgent, seed):
                print("Robots disallowed")
                return
            # CRAWL DELAY
            delay = rp.crawl_delay(userAgent)
            if delay is not None:
                time.sleep(delay)

        # obtain seed content
        htmlContent = None
        htmlHash = ''
        if "html" in response.headers['content-type']:
            driver.get(seed)

            htmlContent = driver.page_source
            htmlHash = hashlib.md5(htmlContent.encode()).hexdigest()

            onClicksList = len(driver.find_elements_by_xpath('//*[@onclick]'))
            if onClicksList != 0:
                for onClickUrl in range(onClicksList):
                    driver.implicitly_wait(5)
                    driver.find_elements_by_xpath('//*[@onclick]')[onClickUrl].click()
                    windows = driver.window_handles

                    if len(windows) > 1:
                        driver.switch_to.window(windows[1])
                    if seed == driver.current_url.replace('www.', ''):
                        continue
                    processFrontier(driver.current_url, option, domains)

                    if len(windows) == 1:
                        driver.back()
                    else:
                        for window in windows[1:]:
                            driver.switch_to.window(window)
                            driver.close()
                    driver.switch_to.window(windows[0])

        driver.quit()

        # detect duplicator by calculating seed canonical form
        # and check if seedCanonicalization has been already visited
        seedCanonicalization = parsed_uri.netloc + parsed_uri.path
        seedCanonicalization = seedCanonicalization + '?' + parsed_uri.query if parsed_uri.query != "" else seedCanonicalization

        # remove trailing slash: e-uprava.gov.si/ == e-uprava.gov.si
        seedCanonicalization = seedCanonicalization[:-1] if seedCanonicalization.endswith('/') else seedCanonicalization

        if getCanonUrl(seedCanonicalization) is not None:
            pageTypeCode = 'DUPLICATE'
            htmlContent = None
        else:
            pageTypeCode = 'FRONTIER'

        # insert into table
        nextPageId = insertPage(site, pageTypeCode, seed, htmlContent, response.status_code, datetime.datetime.now(), htmlHash, seedCanonicalization)

    except (WebDriverException, TimeoutException) as error:
        print(error)
        return None

    return nextPageId
