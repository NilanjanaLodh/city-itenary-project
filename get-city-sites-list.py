from Scrapers import CityScraper
from citylist import cities

def main():
    
    for city in cities:
        print 'collecting data for {}'.format(city)
        scraper = CityScraper(city)
        scraper.fetch_location()
        scraper.get_sites_list()
        scraper.save_to_disk()

main()
