# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import City,OpenCloseTime,PointOfInterest,Photo,Type

admin.site.register(City)
admin.site.register(OpenCloseTime)
admin.site.register(PointOfInterest)
admin.site.register(Photo)
admin.site.register(Type)

# Register your models here.
