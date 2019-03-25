# WIER-1. seminar

Python crawler, which crawls over various .gov.si sites and collects images and binary files.


## Installation

Required python libraries:
* requests
* urllib
* wget
* Image
* xml.etree.ElementTree
* selenium

Selenium in this project uses [ChromeDriver](http://chromedriver.chromium.org/downloads) for the headless browser.


## Usage
Example usage of the crawler. In seedPages you list the sites you wish to crawl,  option can be set as 0 or 1 where 0 means the crawler will only crawl in its own domain and 1 means that the crawler will search over the whole ".gov.si" domain. Using the threadNumber variable you can set the number of threads.
```python
seedPages = ['http://e-uprava.gov.si', 'http://www.evem.gov.si']
option = 0
domains = seedPages
threadsNumber = 4
```
