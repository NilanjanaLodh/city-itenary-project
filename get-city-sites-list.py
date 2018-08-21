from Scrapers import CityScraper


def main():
    # Barcelona
    cities = [ 'Bangkok',  'Paris' 'Milan' , 'London', 'Shanghai', 'New York', 'Amsterdam', 'Istanbul',
        'Tokyo', 'Dubai', 'Vienna', 'Kuala Lumpur',
        'Hong Kong', 'Riyadh','Los Angeles'
    ]
    for city in cities:
        print 'collecting data for {}'.format(city)
        scraper = CityScraper(city)
        scraper.fetch_location()
        scraper.get_sites_list()
        scraper.save_to_disk()

main()
