#!/usr/bin/python
from PIL import Image
import os, sys

path = "/Users/aditya.ra/Documents/training_project/city-itenary-project/travelItenerary/static/img/data/"

for root, dirs, files in os.walk(path):
    for item in files:
        if ".jpeg" in item:
            print item
            path = os.path.join(root, item)
            try:
                im = Image.open(path).convert('RGB')
                imResize = im.resize((1500, 1500), Image.ANTIALIAS)
                imResize.save(path, 'JPEG', quality=90)
            except:
                print ">>>>" + item

