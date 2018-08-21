# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
from datetime import date
from django.utils.translation import gettext as _

class City(models.Model):
	city_name = models.CharField(max_length=40, primary_key=True)

	def __str__(self):
		return '%s' % self.city_name


class Type(models.Model):
	type_name = models.CharField(max_length=20, primary_key=True)

	def __str__(self):
		return '%s' % self.type_name.replace("_", " ")

class PointOfInterest(models.Model):
	POI_id = models.TextField(primary_key=True)
	POI_image_src = models.URLField()
	POI_name = models.CharField(max_length=40)
	formatted_address = models.TextField()
	formatted_phoneNo = models.CharField(max_length=15)
	latitude = models.DecimalField( max_digits=5, decimal_places=2)
	longitude = models.DecimalField( max_digits=5, decimal_places=2)
	no_people_who_rated = models.IntegerField(default = 1)
	rating = models.DecimalField(max_digits = 2, decimal_places = 1)
	POI_map_url = models.URLField()
	POI_website_url = models.URLField()
	types = models.ManyToManyField(Type,null=True,blank=True)
	POI_city = models.ForeignKey(City,on_delete=models.CASCADE, verbose_name = "point of interest of the corresponding city",null=True,blank=True)
	average_time_spent = models.DecimalField(max_digits=4, decimal_places=2, default=0)
	description = models.TextField()

	def __str__(self):
		return '%s' % self.POI_name

class OpenCloseTime(models.Model):
	open_time = models.IntegerField()
	close_time = models.IntegerField()
	day = models.IntegerField()
	POI = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, verbose_name="the opening and closing time of the corresponding point of interest on a certain day",null=True,blank=True)


class Photo(models.Model):
	photo_id = models.TextField(primary_key=True)
	height = models.IntegerField()
	width = models.IntegerField()
	photo_src = models.URLField()
	POI = models.ForeignKey(PointOfInterest,on_delete=models.CASCADE, verbose_name="photo of corresponding point of interest",null=True,blank=True)

class Form(models.Model):
	city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
    )
	start_date = models.DateField(_("Start Date"), default=date.today)
	end_date = models.DateField(_("End Date"), default=date.today)
	type_tags = models.ManyToManyField(Type,null=True,blank=True)

class DistanceTime(models.Model):
	source = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, related_name = "source_set",null=True,blank=True)
	dest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, related_name = "dest_set",null=True,blank=True)
	distance = models.DecimalField(max_digits=15, decimal_places = 2)
	time = models.IntegerField()



# Create your models here.
