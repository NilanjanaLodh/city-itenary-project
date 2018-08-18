## python 2
import requests
import  json
from pprint import pprint
from PIL import Image
from io import BytesIO, StringIO
import os
import time

keynum = 0;
api_keys =  [
    'AIzaSyA8Bx31m2GEuPiRMDuEgpd-9v7fjX1HSMk' #sid
    #'AIzaSyBgzJs6GLkewQeS6y4aPPVvB_QqAMAPYxc',
    #'AIzaSyD1L47J3nVjvAB9JXebI5-P9NCMbPvcZ3k',
    #'AIzaSyBJu3JMPYn4N4VKL3BYp1-j3l-ccjXh4dI'
];
datadir ='./data'

def get_api_key():
    global keynum
    global api_keys
    keynum += 1
    keynum %= len(api_keys)
    time.sleep(10)
    return api_keys[keynum]


def fetch_photo(photo_reference , filename):
    params = {
        'key' : get_api_key(),
        'photoreference' : photo_reference,
        'maxheight' : 500
    }; 
    response = requests.get('https://maps.googleapis.com/maps/api/place/photo', params)
    i = Image.open(BytesIO(response.content))
    Image.save(filename)


class Site_Scraper:
    def __init__(self,site_place_id):
        self.site_place_id = site_place_id
    
    def fetch_details(self):
        params = {
            'key' : get_api_key(),
            'placeid' : self.site_place_id
        };
        response = requests.get('https://maps.googleapis.com/maps/api/place/details/json' , params).json()
        pprint(response)

    


class CityScraper:

    def __init__(self, cityName):
        self.city = cityName;

    def fetch_location(self):
        params = {
            'key' : get_api_key(),
            'input' : self.city,
            'inputtype' : 'textquery',
            'fields' : 'geometry,place_id'
        }
        response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json' , params).json()
        pprint(response)
        self.city_place_id = response["candidates"][0]["place_id"]
        self.lat = response["candidates"][0]["geometry"]["location"]["lat"];
        self.lng = response["candidates"][0]["geometry"]["location"]["lng"];



    def get_sites_list(self):
        params = {
            'key' : get_api_key(),
            'location' : '{},{}'.format(self.lat , self.lng),
            'keyword' : 'things to do in {}'.format(self.city),
            'radius' : 10000,
            'rankby' : 'prominence'    
        }

        response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json' , params).json()
        self.sites = []
        for site in response['results']:
            self.sites.append({
                'name' : site['name'],
                'place_id'   : site['place_id'],
                'location' : {
                    'lat' : site['geometry']['location']['lat'],
                    'lng' : site['geometry']['location']['lng']
                }
            })
        #pprint(response)

    def display(self):
        print self.city
        print self.city_place_id
        print self.lat 
        print self.lng

    def save_to_disk(self):
        
        info = json.dumps(
            {
                'name' : self.city,
                'place_id' : self.city_place_id,
                'lat': self.lat,
                'lng' : self.lng
            }
        );
        dirname = '{}/{}'.format(datadir, self.city);
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open('{}/info.json'.format(dirname) , 'w+') as f:
            f.write(info)

        with open('{}/sites.json'.format(dirname) , 'w+' ) as f:
            f.write(json.dumps(self.sites))

def main():
    
    # Barcelona
    cities = [ 'Bangkok', 'Seoul',  'Paris' 'Milan' , 'London', 'Shanghai', 'New York', 'Amsterdam', 'Istanbul',
        'Tokyo', 'Dubai', 'Vienna', 'Kuala Lumpur',
        'Hong Kong', 'Riyadh','Los Angeles'
    ];
    for city in cities:
        print 'collecting data for {}'.format(city)
        scraper = CityScraper(city)
        scraper.fetch_location()
        scraper.get_sites_list()
        scraper.save_to_disk()
    



main()