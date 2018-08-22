##python 3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup as bs
from time import sleep
import json
import os

driver = webdriver.Chrome()
driver.get("http://www.google.com")

def get_rating_num(placeQueryString):
    inputElem = driver.find_element_by_name("q")
    inputElem.clear()
    inputElem.send_keys(placeQueryString)
    inputElem.submit()
    WebDriverWait(driver, 10).until(EC.title_contains(placeQueryString))
    soup = bs(driver.page_source , 'html.parser')
    try:
        return soup.find_all('a', {'jsaction':'r.BMsjWllwe1s'})[0].span.text.split(' ')[0].replace(',','')
    except:
        return '1'

from citylist import cities
from newdatadir import datadir

def ensure_site_dir_exists(city,siteName):
    siteDir = '{}/{}/sites/{}'.format(datadir,city,siteName)
    if not os.path.exists(siteDir):
        os.makedirs(siteDir)
    return siteDir



for city in cities:
    print(city)
    sitesfile = open('{}/{}/sites.json'.format(datadir, city),'r')
    siteslist = json.load(sitesfile)
    for site in siteslist:
        print(site['name']) 
        sleep(1)
        rating_n = get_rating_num(site['name'] + ' ' + city)
        siteDir = ensure_site_dir_exists(city, site['name'])
        with open('{}/rating_n'.format(siteDir), 'w+') as f:
            f.write(rating_n)

driver.quit()