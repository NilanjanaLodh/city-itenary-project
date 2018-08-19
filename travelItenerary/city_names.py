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
                if "rating" not in json_data:
                    city = City(city_name = json_data['name'])
                    try:
                        city.save()
                    except:
                        pass


