# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

class City(models.Model):
	city_name = models.CharField(max_length=40)

	def __str__(self):
		return '%s' % self.city_name


class Type(models.Model):
	type_name = models.CharField(max_length=20)

	def __str__(self):
		return '%s' % self.type_name

class PointOfInterest(models.Model):
	POI_id = models.TextField()
	POI_image_src = models.URLField()
	POI_name = models.CharField(max_length=40)
	formatted_address = models.TextField()
	formatted_phoneNo = models.CharField(max_length=15)
	latitude = models.DecimalField( max_digits=5, decimal_places=2)
	longitude = models.DecimalField( max_digits=5, decimal_places=2)
	rating = models.DecimalField(max_digits = 2, decimal_places = 1)
	POI_map_url = models.URLField()
	POI_website_url = models.URLField()
	types = models.ManyToManyField(Type)
	POI_city = models.ForeignKey(City,on_delete=models.CASCADE, verbose_name = "point of interest of the corresponding city",default=0)

	def __str__(self):
		return '%s' % self.POI_name

class OpenCloseTime(models.Model):
	open_time = models.IntegerField()
	close_time = models.IntegerField()
	day = models.IntegerField()
	POI = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, verbose_name="the opening and closing time of the corresponding point of interest on a certain day",)


class Photo(models.Model):
	photo_id = models.TextField()
	height = models.IntegerField()
	width = models.IntegerField()
	photo_src = models.URLField()
	POI = models.ForeignKey(PointOfInterest,on_delete=models.CASCADE, verbose_name="photo of corresponding point of interest")

class Form(models.Model):
	city = models.OneToOneField(
        City,
        on_delete=models.CASCADE,
        related_name='city entered for itenerary',
    )
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    type_tags = models.ManyToManyField(Type)


# Create your models here.
