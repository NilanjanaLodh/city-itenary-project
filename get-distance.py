import os
import requests
from time import sleep
import json

api_key = 'AIzaSyBh9jfDgzqM654rjJIpf89VWOwtneaB-6g'
datadir = './data'

def get_api_key():
    global api_key
    sleep(0.4)
    return api_key


def get_distance(site1 , site2):
    params = {
        'origins' : '{},{}'.format(site1[0] , site1[1]),
        'destinations': '{},{}'.format(site2[0] , site2[1]),
        'units' : 'metric',
        'key': get_api_key()
    }

    response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json', params).json()
    
    try:
        return (response['rows'][0]['elements'][0]['duration']['value']/60 , #mins
        response['rows'][0]['elements'][0]['distance']['value'])#in meters
    except:
        print response
        return (-1,-1)

#get_distance((40.6655101,-73.89), (40.6905615,-73.9976592))


def get_distances_for_city(cityname):
    sitesfile = open('{}/{}/sites.json'.format(datadir, cityname),'r')

    siteslist = json.load(sitesfile)
    with open('{}/{}/dist.json'.format(datadir, cityname), 'w+') as distfile:
        for site1 in siteslist:
            for site2 in siteslist:
                placeid1 = site1['place_id']
                placeid2 = site2['place_id']
                if placeid1 != placeid2:
                    print site1['place_id'] , site2['place_id']
                    time, dist = get_distance((site1['location']['lat'],site1['location']['lng']),
                                (site2['location']['lat'],site2['location']['lng']))
                    
                    distfile.write(json.dumps({
                       'source' : site1['place_id'],
                       'dest'   : site2['place_id'],
                       'time'   : time,
                       'dist'   : dist
                    })+'\n')
                


#ignore seoul ; google maps not available here
cities = [ 'Shanghai', 'London',  'New York', 'Amsterdam', 'Istanbul','Tokyo', 
    'Dubai', 'Vienna', 'Kuala Lumpur',
    'Los Angeles', 'Paris', 'Milan','Hong Kong','Riyadh'
]

for city in cities:
    print city
    get_distances_for_city(city)