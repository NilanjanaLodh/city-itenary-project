## python 3
import populartimes
from statistics import mean
from time import sleep
import json

datadir = './data'
api_key =  'AIzaSyBh9jfDgzqM654rjJIpf89VWOwtneaB-6g'
newfile = 'new_info.json'

def get_api_key():
    global api_key
    sleep(1)
    return api_key


def fetch_new_info(placeid):
    response = populartimes.get_id(get_api_key(),placeid)
    new_info = {
        'id' : response['id'],
        'name' : response['name'],
        'lat' : response['coordinates']['lat'],
        'lng': response['coordinates']['lng']
    }

    optfields = [
        'rating',
        'rating_n',
        'types',
        'address'
    ]
    for field in optfields:
        if field not in response:
            print('no {}'.format(field))
        else:
            new_info[field] = response[field]

    if 'time_spent' not in response:
        print('no time spent')
    else:
        new_info['avg_time_spent'] = mean(response['time_spent'])
    return new_info

cities = [ 'Bangkok',  'Paris' , 'Milan' , 'London', 'Shanghai', 'New York', 'Amsterdam', 'Istanbul',
        'Tokyo', 'Dubai', 'Vienna', 'Kuala Lumpur',
        'Hong Kong', 'Riyadh','Los Angeles'
    ]

for city in cities:
        print('\n\ncity {}'.format(city))
        citydir = '{}/{}'.format(datadir, city)
        with open( '{}/sites.json'.format(citydir), 'r') as f:
            sites_list = json.load(f)
            for site in sites_list:
                place_id = site['place_id']
                print('placeid {}'.format(place_id))
                new_info = fetch_new_info(place_id)
                with open('{}/sites/{}/new_info.json'.format(citydir,place_id), 'w+') as f:
                    f.write(json.dumps(new_info))