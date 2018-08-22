##python 3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup as bs
from time import sleep
import json
import os

from citylist import cities
from newdatadir import datadir

driver = webdriver.Chrome()


def get_sites_list(city):
    #First search on google
    queryString = 'best places to visit in {}'.format(city)
    driver.get("http://www.google.com")
    inputElem = driver.find_element_by_name("q")
    inputElem.send_keys(queryString)
    inputElem.submit()
    WebDriverWait(driver, 10).until(EC.title_contains(queryString))
    

    #then search for 'More things to do'
    soup = bs(driver.page_source , 'html.parser')
    moreThingsToDoImg = soup.find('img', {'class': 'KJ3c0b'})
    moreThingsToDoLink = 'http://www.google.com'+ moreThingsToDoImg.parent['href']
    #visit the more things to do link
    driver.get(moreThingsToDoLink)
    WebDriverWait(driver, 10).until(EC.title_contains(city))
    
    
    #then parse the results
    soup = bs(driver.page_source , 'html.parser')
    results = soup.select('li[class*="zb2Jbd imyN8d"]')

    sites = []
    rank = 1
    for result in results:
        info = {}
        info['name'] = result.div.div.div.h2.text
        try:
            info['tagline'] = result.div.div.p.text

            if result.div.div.p.find_next('p').parent == result.div.div :
                info['description'] = result.div.div.p.find_next('p').contents[0]
            else:
                info['description'] = ''
        except:
            info['tagline'] = ''
            info['description'] = ''
        
        info['rank'] = rank
        sites.append(info)
        rank += 1
    return sites


def iterate_over_cities():
    for city in cities:
        sleep(1)
        print(city)
        try:
            sitesList = get_sites_list(city)
            write_sites_list_to_file(city , sitesList)
        except Exception as e:
            print(e)
            print('>>>>>failed')


def write_sites_list_to_file(city, sitesList):
    cityDir = ensure_city_dir_exists(city)
    sitesFileName = '{}/sites.json'.format(cityDir)
    with open(sitesFileName, 'w+') as f:
        f.write(json.dumps(sitesList))    

def ensure_city_dir_exists(city):
    cityDir = '{}/{}'.format(datadir,city)
    if not os.path.exists(cityDir):
        os.makedirs(cityDir)
    return cityDir

try:
    iterate_over_cities()
finally:
    driver.quit()

# print(get_sites_list('Dubai'))
# driver.quit()