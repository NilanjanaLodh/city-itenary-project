import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

data_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/data"

for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "info" in file_name:
            with open(file_name) as data:
                json_data = json.load(data)
                if "rating" in json_data:
                    new_poi = PointOfInterest()
                    new_poi.POI_id = os.path.dirname(file_name).split('/')[-1]
                    new_poi.POI_name = json_data['name']
                    new_poi.latitude = json_data['lat']
                    new_poi.longitude = json_data['lng']
                    new_poi.rating = json_data['rating']
                    new_poi.POI_city = City.objects.get(city_name = os.path.dirname(file_name).split('/')[-3])
                    
                    new_poi.save()
                    
                    poi_types = json_data['types']
                    for poi_type in poi_types:
                        new_poi.types.add(poi_type)






