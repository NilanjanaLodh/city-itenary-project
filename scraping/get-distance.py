import os
import requests
from time import sleep
import json

api_key = 'AIzaSyBh9jfDgzqM654rjJIpf89VWOwtneaB-6g'
from newdatadir import datadir

def get_api_key():
    global api_key
    sleep(0.0006)
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
                with open(u'{}/{}/sites/{}/info.json'.format(datadir,city,site1['name']),'r') as f1:
                    info1 =json.load(f1)
                with open(u'{}/{}/sites/{}/info.json'.format(datadir,city,site2['name']),'r') as f2:
                    info2 =json.load(f2)

                if info1['place_id'] != info2['place_id']:
                    print site1['name'] , site2['name']
                   
                    time, dist = get_distance((info1['lat'], info1['lng']) , (info2['lat'], info2['lng']))
                    
                    distfile.write(json.dumps({
                       'source' : info1['place_id'],
                       'dest'   : info2['place_id'],
                       'time'   : time,
                       'dist'   : dist
                    })+'\n')
                


from citylist import cities
for city in cities[11:]:
    print city
    get_distances_for_city(city)