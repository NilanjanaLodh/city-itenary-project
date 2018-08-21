## python 2
import requests
import json
from pprint import pprint
from PIL import Image
from io import BytesIO, StringIO
import os
import time

keynum = 0;
api_keys = [
    #'AIzaSyA8Bx31m2GEuPiRMDuEgpd-9v7fjX1HSMk'  # sid
     'AIzaSyBh9jfDgzqM654rjJIpf89VWOwtneaB-6g' # arvan
    #, 'AIzaSyBgzJs6GLkewQeS6y4aPPVvB_QqAMAPYxc'
    #, 'AIzaSyD1L47J3nVjvAB9JXebI5-P9NCMbPvcZ3k'
    #, 'AIzaSyBJu3JMPYn4N4VKL3BYp1-j3l-ccjXh4dI'
];
datadir = './data'


def get_api_key():
    global keynum
    global api_keys
    keynum += 1
    keynum %= len(api_keys)
    time.sleep(.5)
    return api_keys[keynum]



class SiteScraper:
    def __init__(self, site_place_id, citydir):
        self.site_place_id = site_place_id
        self.dir = '{}/sites/{}'.format(citydir, site_place_id)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def fetch_details(self):


        params = {
            'key': get_api_key(),
            'place_id': self.site_place_id
        }
        response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params).json()['result']
        self.photo_references = []

        if 'photos' in response:
            for photo in response['photos']:
                self.photo_references.append(photo['photo_reference'])

        if os.path.exists('{}/info.json'.format(self.dir)):
            print 'already fetched!'
            return

        self.info = {
            'name': response['name'],
            'lat': response['geometry']['location']['lat'],
            'lng': response['geometry']['location']['lng'],
            'northeast_corner': response['geometry']['viewport']['northeast'],
            'southwest_corner': response['geometry']['viewport']['southwest'],
            'types': response['types']
        }
        if 'rating' in response:
            self.info['rating']= response['rating']
            
        if 'opening_hours' in response:
            self.info['timings'] = response['opening_hours']['periods']
        print '\n'

        with open('{}/info.json'.format(self.dir), 'w+') as f:
            f.write(json.dumps(self.info))
            f.close()



    def fetch_photos(self):

        count = 0
        for photo_reference in self.photo_references:
            count += 1

            if not os.path.exists('{}/{}.jpeg'.format(self.dir, count)):
                print '\tfetching photo {}'.format(photo_reference)
                params = {
                    'key': get_api_key(),
                    'photoreference': photo_reference,
                    'maxheight': 1000
                }
                response = requests.get('https://maps.googleapis.com/maps/api/place/photo', params)

                with open('{}/{}.jpeg'.format(self.dir, count), 'wb') as f:
                    f.write(response.content)

            if count == 5:
                break



class CityScraper:

    def __init__(self, cityName):
        self.city = cityName;

    def fetch_location(self):
        params = {
            'key': get_api_key(),
            'input': self.city,
            'inputtype': 'textquery',
            'fields': 'geometry,place_id'
        }
        response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params).json()
        pprint(response)
        self.city_place_id = response["candidates"][0]["place_id"]
        self.lat = response["candidates"][0]["geometry"]["location"]["lat"];
        self.lng = response["candidates"][0]["geometry"]["location"]["lng"];

    def get_sites_list(self):
        params = {
            'key': get_api_key(),
            'location': '{},{}'.format(self.lat, self.lng),
            'keyword': 'things to do in {}'.format(self.city),
            'radius': 10000,
            'rankby': 'prominence'
        }

        response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params).json()
        self.sites = []
        for site in response['results']:
            self.sites.append({
                'name': site['name'],
                'place_id': site['place_id'],
                'location': {
                    'lat': site['geometry']['location']['lat'],
                    'lng': site['geometry']['location']['lng']
                }
            })
        # pprint(response)

    def display(self):
        print self.city
        print self.city_place_id
        print self.lat
        print self.lng

    def save_to_disk(self):

        info = json.dumps(
            {
                'name': self.city,
                'place_id': self.city_place_id,
                'lat': self.lat,
                'lng': self.lng
            }
        )
        dirname = '{}/{}'.format(datadir, self.city);
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open('{}/info.json'.format(dirname), 'w+') as f:
            f.write(info)

        with open('{}/sites.json'.format(dirname), 'w+') as f:
            f.write(json.dumps(self.sites))
