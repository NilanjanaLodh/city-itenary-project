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
        if "rating" in file_name:
            with open(file_name) as data:
                count = int(data.readlines()[0])
                poi_id = os.path.dirname(file_name).split('/')[-1]
                poi = PointOfInterest.objects.get(POI_id = poi_id)
                poi.no_people_who_rated = count
                poi.save()

