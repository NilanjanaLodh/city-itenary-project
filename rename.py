import json
import os


cities = [ 'Bangkok' , 'Singapore' , 'Rome' , 'Taipei', 
    'Shanghai', 'London',  'New York', 'Amsterdam', 'Istanbul','Tokyo', 
    'Dubai', 'Vienna', 'Kuala Lumpur',
    'Los Angeles', 'Paris', 'Milan','Hong Kong','Riyadh']
datadir = './data'
for city in cities:
    print(city)
    sitesfile = open('{}/{}/sites.json'.format(datadir, city),'r')
    siteslist = json.load(sitesfile)
    for site in siteslist:
        os.rename('{}/{}/sites/{}/avg_rating'.format(datadir , city , site['place_id']),
           '{}/{}/sites/{}/avg_time'.format(datadir , city , site['place_id']))