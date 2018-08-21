from Scrapers import SiteScraper
import os
import json

datadir = './data'
def main():
    # Paris, ,'Milan'
    done = [ 'Bangkok', 'London', 'Shanghai', 'New York', 'Amsterdam', 'Istanbul',
        'Tokyo', 'Dubai', 'Vienna', 'Kuala Lumpur',
        'Hong Kong', 'Riyadh','Los Angeles', 'Paris' , 'Milan'
    ]
    cities = ['Singapore' , 'Taipei' , 'Rome']
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

