from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome('chromedriver', options=options)

try:
    driver.get("https://yts.am/")

    # get all parts of HTML that contain information on titles, genres, years...
    elems = driver.find_elements_by_xpath('//div[contains(@class, "browse-movie-wrap")]')

    for elem in elems:
        # some parts doesn't have ratings - check and continue only if there is a rating
        ratings = elem.find_elements_by_class_name('rating')
        if len(ratings) == 1:
            # capture the rating and if it is 7 or more, print the movie title, year and rating
            # rating comes in the following form: "X / 10" where X is the rating.
            rating = float(elem.find_element_by_class_name('rating').get_attribute('innerText').split('/')[0])
            if rating >= 7.0:
                print(elem.find_element_by_class_name('browse-movie-title').text)
                print(elem.find_element_by_class_name('browse-movie-year').text)
                print(rating)

    driver.quit()

except:
    driver.quit()
    raise