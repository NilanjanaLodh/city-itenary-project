import requests
import json
from pprint import pprint
from PIL import Image
from io import BytesIO, StringIO
import os
from time import sleep
from citylist import cities
from newdatadir import datadir
from shutil import copyfile

apiKey = 'AIzaSyBh9jfDgzqM654rjJIpf89VWOwtneaB-6g'

def get_api_key():
    global apiKey
    sleep(0.1)
    return apiKey

def filter_types(types):
    allowed_types =[
        'amusement_park',
        'aquarium',
        'art_gallery',
        'bakery',
        'bar',
        'book_store',
        'cafe',
        'casino',
        'cemetery',
        'church',
        'city_hall',
        'mosque',
        'museum',
        'night_club',
        'park',
        'shopping_mall',
        'stadium',
        'synagogue',
        'natural_feature',
        'place_of_worship',
        'zoo'
    ]

    filtered_types = []
    for t in types:
        if t in allowed_types:
            filtered_types.append(t)

    return filtered_types
 
def get_site_details(city , site):
    info = {}
    params = {
        'key' : get_api_key(),
        'input' : site + ' ' + city,
        'inputtype' : 'textquery',
        'fields' : 'place_id,geometry/location,types,rating'
    }
    response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params).json()['candidates'][0]
    info['place_id'] = response['place_id']
    info['lat'] = response['geometry']['location']['lat']
    info['lng'] = response['geometry']['location']['lng']
    
    if 'rating' in response:
        info['rating'] = response['rating']
    else:
        info['rating'] = 3
    
    if 'types' in response:
        info['types'] = filter_types(response['types'])

    return info
    


def check_if_old_photos_exist(city , placeId):
    oldPhotosDir = u'../data/{}/sites/{}'.format(city,placeId)
    if os.path.exists(oldPhotosDir):
        return oldPhotosDir
    else:
        return None


def copy_photos(oldPhotosDir , city , site):
    for count in range(1,6):
        print 'copying {}.jpeg'.format(count)
        copyfile(u'{}/{}.jpeg'.format(oldPhotosDir,count) ,
                 u'{}/{}/sites/{}/{}.jpeg'.format(datadir,city,site,count))

def fetch_photos(city , site , placeId):
    oldPhotosDir = check_if_old_photos_exist(city , placeId)
    if oldPhotosDir is None:
        params = {
            'key': get_api_key(),
            'place_id': placeId,
            'fields' : 'photos'
        }
        response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params).json()['result']
        photo_references = []
        if 'photos' in response:
            for photo in response['photos']:
                photo_references.append(photo['photo_reference'])
        
        count = 0
        for photo_reference in photo_references:
            count += 1
            photoFile = u'{}/{}/sites/{}/{}.jpeg'.format(datadir,city,site, count)
            if not os.path.exists(photoFile):
                print '\tfetching photo {}'.format(photo_reference)
                params = {
                    'key': get_api_key(),
                    'photoreference': photo_reference,
                    'maxheight': 1000
                }
                response = requests.get('https://maps.googleapis.com/maps/api/place/photo', params)
                try:
                    with open(photoFile,'wb') as f:
                        f.write(response.content)
                except:
                    print 'couldnt fetch photo'
                    count -= 1
                
            if count == 5:
                break
        
    else :
        copy_photos(oldPhotosDir , city , site)

def get_site_list_from_json(city):
    with open(u'{}/{}/sites.json'.format(datadir,city), 'r') as f:
        sitesList = [site['name'] for site in json.load(f)]

    return sitesList

def try_if_info_fetched_before(infoFileName):
    if os.path.exists(infoFileName):
        with open(infoFileName, 'r') as f:
            info = json.load(f)
        return info 
    else:
        return None
        

def iterate_over_cities():
    for city in cities[3:]:
        sitesList = get_site_list_from_json(city)
        for site in sitesList:
            print site
            infoFileName = u'{}/{}/sites/{}/info.json'.format(datadir,city,site)
            info = try_if_info_fetched_before(infoFileName)
            if info is None:
                info = get_site_details(city , site)
            print info
            fetch_photos(city,site,info['place_id'] )
            with open(infoFileName, 'w+') as f:
                f.write(json.dumps(info))
            

iterate_over_cities()