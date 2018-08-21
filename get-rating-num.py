##python 3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup as bs
from time import sleep
import json

driver = webdriver.Chrome()
driver.get("http://www.google.com")

def get_rating_num(placeQueryString):
    inputElem = driver.find_element_by_name("q")
    inputElem.clear()
    inputElem.send_keys(placeQueryString)
    inputElem.submit()
    sleep(5)
    soup = bs(driver.page_source , 'html.parser')
    try:
        return soup.find_all('a', {'jsaction':'r.BMsjWllwe1s'})[0].span.text.split(' ')[0].replace(',','')
    except:
        return '1'


#ignore seoul ; google maps not available here
cities = [ 'Bangkok' , 'Singapore' , 'Rome' , 'Taipei', 
    'Shanghai', 'London',  'New York', 'Amsterdam', 'Istanbul','Tokyo', 
    'Dubai', 'Vienna', 'Kuala Lumpur',
    'Los Angeles', 'Paris', 'Milan','Hong Kong','Riyadh']
datadir = './data'
for city in cities:
    print(city)
    sitesfile = open('{}/{}/sites.json'.format(datadir, city),'r')
    siteslist = json.load(sitesfile)
    for site in siteslist:
        print(site['name'] + ' ' + site['place_id']) 
        sleep(1)
        rating_n = get_rating_num(site['name'] + ' ' + city)
        with open('{}/{}/sites/{}/rating_n'.format(datadir , city , site['place_id']), 'w+') as f:
            f.write(rating_n)