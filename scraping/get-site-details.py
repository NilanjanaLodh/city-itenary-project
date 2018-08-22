from Scrapers import SiteScraper
import os
import json
from citylist import cities

datadir = './data'
def main():
    # Paris, ,'Milan'
    for city in cities:
        print '\n\nscraping city {}'.format(city)
        citydir = '{}/{}'.format(datadir, city)
        with open( '{}/sites.json'.format(citydir), 'r') as f:
            sites_list = json.load(f)
            for site in sites_list:
                place_id = site['place_id']
                print 'scraping placeid {}'.format(place_id)
                scraper = SiteScraper(place_id, citydir)
                scraper.fetch_details()
                scraper.fetch_photos()





main()

