# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.template import loader
from .iteneraryform import IteneraryForm
import json
from .itenerary_generator import generate_itenerary
from models import *
import os, copy
from django.conf import settings

plan = {}
# Create your views here.
# plan = {
#     "city": "Dubai",
#     "start_date": "08/21/2018",
#     "days": 2,
#     "tour":[
#                 [
#                     {
#                         "lat": 25.242992, 
#                         "lng": 55.33269 ,
#                         "name": "Park Hyatt Dubai", 
#                         "place_id": "ChIJ90SK0zxdXz4REVAnXhulhJQ", 
#                         "rating": 5,
#                         "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
#                         "time": "time_to_visit",
#                         "cost": "cost"
#                     },
#                     {
#                         "lat": 25.197405, 
#                         "lng": 55.274331 ,
#                         "name" : "At the top of burj khalifa",
#                         "place_id": "ChIJK_3sryxoXz4Ra2EynnqG6UQ", 
#                         "rating": 3,
#                         "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
#                         "time": "time_to_visit",
#                         "cost": "cost"

#                     },
#                     {
#                         "name": "The Dubai Mall", 
#                         "lat": 25.198518, 
#                         "lng": 55.279619,
#                         "place_id": "ChIJB1zIKShoXz4RnbaTPPup7aU", 
#                         "rating": 4,
#                         "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
#                         "time": "time_to_visit",
#                         "cost": "cost"
#                     },
#                     {
#                         "lat": 25.1330986, 
#                         "lng": 55.183466 , "name": "Madinat Jumeirah",
#                         "place_id": "ChIJORSp9gBCXz4RtnTCn-ul3mo", 
#                         "rating": 4,
#                         "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
#                         "time": "time_to_visit",
#                         "cost": "cost"
#                     }
#                 ],
#                 [
#                     {
#                         "lat": 25.139409, 
#                         "lng": 55.188844 , 
#                         "name": "Wild wadi waterpark",
#                         "place_id": "ChIJh7LUHlFqXz4RbIRg-g5fo-E", 
#                         "rating": 5,
#                         "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
#                         "time": "time_to_visit",
#                         "cost": "cost"
#                     },
#                     {
#                         "lat": 25.1971411, 
#                         "lng": 55.2796665 , 
#                         "name" : "Dubai ice rink",
#                         "place_id": "ChIJ0Yv9GShoXz4R5t9gYCGvNHs", 
#                         "rating": 2,
#                         "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
#                         "time": "time_to_visit",
#                         "cost": "cost"
#                     }
#                 ]
#     ]
# }

def get_image_url(city, place_id, ct):
    return "img/data/" + city + "/sites/" + place_id + "/" + ct + ".jpeg"

def add_images_rating(given_plan):
    for day in given_plan['tour']:
        for place in day:
            place['rating_len'] = range(int(round(float(place['rating']))))
            place['images'] = []
            for i in range(0, 4):
                place['images'].append(get_image_url(given_plan['city'], place['place_id'], str(i+1)))
            place['lat'] = float(place['lat'])
            place['lng'] = float(place['lng'])
    return given_plan

def am_pm(value):
    hr = int(value)
    mn = int((value*60) % 60)
    mn = mn
    if hr > 12:
        if mn < 10: return str(hr-12) + " : 0" + str(mn) + " pm"
        else: return str(hr-12) + " : " + str(mn) + " pm"
    elif hr == 12:
        if mn < 10: return str(hr) + " : 0" + str(mn) + " pm"
        else: return str(hr) + " : " + str(mn) + " pm"
    else:
        if mn < 10: return str(hr) + " : 0" + str(mn) + " am"
        else: return str(hr) + " : " + str(mn) + " am"



def get_time_string(start, duration):
    time_string = ""
    time_string += am_pm(start + 9.00) + " to "
    time_string += am_pm(start + 9.00 + duration) 
    return time_string

def correct_time_format(given_plan):
    for day in given_plan['tour']:
        for place in day:
            time_spent = PointOfInterest.objects.get(POI_id = place['place_id']).average_time_spent
            place['time_to_show'] = get_time_string(float(place['time']), float(time_spent))
    return given_plan

def get_no_ratings(given_plan):
    for day in given_plan['tour']:
        for place in day:
            n_ratings = PointOfInterest.objects.get(POI_id = place['place_id']).no_people_who_rated
            place['no_of_ratings'] = n_ratings
    return given_plan

def get_timetravel(given_plan):
    for day in given_plan['tour']:
        first = True
        pre_id = ""
        for place in day:
            if first == True:
                first = False
                place['travel_time'] = -1
                place['travel_dist'] = -1
                pre_id = place['place_id']
                continue
            source = PointOfInterest.objects.get(POI_id = pre_id)
            dest = PointOfInterest.objects.get(POI_id = place['place_id'])
            obj = DistanceTime.objects.get(source = source, dest = dest)
            place['travel_dist'] = float(obj.distance) /1000.0
            place['travel_time'] = obj.time
            pre_id = place['place_id']
    return given_plan



def itenerary_form(request): 
    form = IteneraryForm(
        initial = {
            'city': '',
            'start_date': '',
            'end_date': ''
        }
        )
    if request.method == "POST":
        form = IteneraryForm(request.POST)
        if form.is_valid():
            form.save()
            context = dict()
            context['city']= form.cleaned_data.get("city")
            context['start_date'] = form.cleaned_data.get("start_date")
            context['end_date'] = form.cleaned_data.get("end_date")
            context['type_tags'] = form.cleaned_data.get("type_tags")
            global plan
            plan = get_timetravel(get_no_ratings(correct_time_format(add_images_rating(json.loads(generate_itenerary(context))))))
            return HttpResponseRedirect('/iteneraryApplication/show_plan/');
    
        # return render(request, 'templates/index2.html', {'form': itene})
    return render(request, 'index2.html', {'form': form})
    # return render(request, html template page to return after form, params for form)


def show_plan(request):
    #will get the plan from the algorithm
    global plan
    return HttpResponse(loader.get_template("show_plan.html").render(plan))

def thanks(request):
    return HttpResponse("Hello World")

def show_map(request):
    global plan
    tour = plan["tour"]
    return render(request , 'map.html' , {
        'plan' : json.dumps(tour),
        'start_date' : plan['start_date'], #mm/dd/yy
        'city' : plan['city']
    });

from LAplan import laPlan
def show_map_test(request):
    return render(request , 'map.html' , {
        'plan' : json.dumps(laPlan['tour']),
        'start_date' : laPlan['start_date'], #mm/dd/yy
        'city' : laPlan['city']
    });

