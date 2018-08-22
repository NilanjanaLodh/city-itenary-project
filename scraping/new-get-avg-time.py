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

def search_on_tripadvisor(tripadvisorQueryString):
    try:
        print(tripadvisorQueryString)
        driver.get("http://www.google.com")    
        inputElement = driver.find_element_by_name("q")
        inputElement.send_keys(tripadvisorQueryString)
        inputElement.submit()


        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 10).until(EC.title_contains(tripadvisorQueryString))
        soup = bs(driver.page_source , 'html.parser')
        tripAdvisorLink = soup.find_all('h3',{'class':'r'})[0].a['href']
        driver.get(tripAdvisorLink)
        WebDriverWait(driver, 15).until(EC.title_contains('TripAdvisor'))
        soup = bs(driver.page_source , 'html.parser')
        durationSpan = soup.select('span[class*="ui_icon duration"]')[0]
        print(durationSpan)
        durationText = durationSpan.parent.text
        print(durationText)
        durationText = durationText.replace('-',' ')
        times = [int(s) for s in durationText.split(' ') if s.isdigit()]
        return mean(times)
    except:
        return 1

from citylist import cities
from newdatadir import datadir

def ensure_site_dir_exists(city,siteName):
    siteDir = '{}/{}/sites/{}'.format(datadir,city,siteName)
    if not os.path.exists(siteDir):
        os.makedirs(siteDir)
    return siteDir

def site_already_fetched(city,siteName):
    return os.path.exists('{}/{}/sites/{}/avg_time'.format(datadir,city,siteName))



for city in cities:
    print(city)
    sitesfile = open('{}/{}/sites.json'.format(datadir, city),'r')
    siteslist = json.load(sitesfile)
    for site in siteslist:
        print(site['name']) 
        sleep(0.5)
        if not site_already_fetched(city,site['name']):
            avg_time = search_on_tripadvisor(site['name'] + ' ' + city+ ' attraction tripadvisor')
            siteDir = ensure_site_dir_exists(city, site['name'])
            with open('{}/avg_time'.format(siteDir), 'w+') as f:
                f.write(str(avg_time))

driver.quit()