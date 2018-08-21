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
        if "avg_time" in file_name:
            with open(file_name) as data:
                time = float(data.readlines()[0])
                poi_id = os.path.dirname(file_name).split('/')[-1]
                poi = PointOfInterest.objects.get(POI_id = poi_id)
                poi.average_time_spent = time
                poi.save()

