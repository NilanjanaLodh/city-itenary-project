# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.template import loader
from .iteneraryform import IteneraryForm
import json
from .itenerary_generator import generate_itenerary, modify_itenerary, generate_POI_dict
from models import *
import os, copy
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from get_POI import get_POIs, get_POI_object
from django.http import Http404

# Create your views here.
plan = {
    'city': 'Los Angeles', 
    'tour': 
    [
        [
            {
                'travel_time': 0,
                'rating': '4.7',
                'name': 'STAPLES Center',
                'time_to_show': '9 : 00 am to 10 : 00 am',
                'time_spent': 1,
                'place_id': 'ChIJkyrqXbjHwoAR1bJ76zx89B8',
                'travel_dist': 0,
                'no_of_ratings': 9615,
                'images': ['img/data/Los Angeles/sites/ChIJkyrqXbjHwoAR1bJ76zx89B8/1.jpeg', 'img/data/Los Angeles/sites/ChIJkyrqXbjHwoAR1bJ76zx89B8/2.jpeg', 'img/data/Los Angeles/sites/ChIJkyrqXbjHwoAR1bJ76zx89B8/3.jpeg', 'img/data/Los Angeles/sites/ChIJkyrqXbjHwoAR1bJ76zx89B8/4.jpeg'],
                'cost': 10,
                'time': 0,
                'lat': 34.04,
                'lng': -118.27,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            },
            {
                'travel_time': 10,
                'rating': '4.5',
                'name': 'El Pueblo de Los Angeles Historical Monument',
                'time_to_show': '10 : 10 am to 11 : 40 am',
                'place_id': 'ChIJgQpEAUXGwoARoG9LzK0GhV0',
                'time_spent': 1.5,
                'travel_dist': 5.202,
                'no_of_ratings': 957,
                'images': ['img/data/Los Angeles/sites/ChIJgQpEAUXGwoARoG9LzK0GhV0/1.jpeg', 'img/data/Los Angeles/sites/ChIJgQpEAUXGwoARoG9LzK0GhV0/2.jpeg', 'img/data/Los Angeles/sites/ChIJgQpEAUXGwoARoG9LzK0GhV0/3.jpeg', 'img/data/Los Angeles/sites/ChIJgQpEAUXGwoARoG9LzK0GhV0/4.jpeg'],
                'cost': 10,
                'time': '1.166666666666666657414808128',
                'lat': 34.06,
                'lng': -118.24,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            },
            {
                'travel_time': 5,
                'rating': '4.6',
                'name': 'The Broad',
                'time_to_show': '11 : 45 am to 12 : 45 pm',
                'place_id': 'ChIJXaYsEk3GwoARvx7RKBUE8Zg',
                'time_spent': 1,
                'travel_dist': 1.637,
                'no_of_ratings': 4088,
                'images': ['img/data/Los Angeles/sites/ChIJXaYsEk3GwoARvx7RKBUE8Zg/1.jpeg', 'img/data/Los Angeles/sites/ChIJXaYsEk3GwoARvx7RKBUE8Zg/2.jpeg', 'img/data/Los Angeles/sites/ChIJXaYsEk3GwoARvx7RKBUE8Zg/3.jpeg', 'img/data/Los Angeles/sites/ChIJXaYsEk3GwoARvx7RKBUE8Zg/4.jpeg'],
                'cost': 10,
                'time': '2.749999999999999986122212192',
                'lat': 34.05,
                'lng': -118.25,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            },
            {
                'travel_time': 10,
                'rating': '4.7',
                'name': 'Natural History Museum of Los Angeles County',
                'time_to_show': '12 : 55 pm to 3 : 55 pm',
                'place_id': 'ChIJXzARBf3HwoARJyT7uZSV-G4',
                'time_spent': 3,
                'travel_dist': 6.972,
                'no_of_ratings': 3171,
                'images': ['img/data/Los Angeles/sites/ChIJXzARBf3HwoARJyT7uZSV-G4/1.jpeg', 'img/data/Los Angeles/sites/ChIJXzARBf3HwoARJyT7uZSV-G4/2.jpeg', 'img/data/Los Angeles/sites/ChIJXzARBf3HwoARJyT7uZSV-G4/3.jpeg', 'img/data/Los Angeles/sites/ChIJXzARBf3HwoARJyT7uZSV-G4/4.jpeg'],
                'cost': 10,
                'time': '3.916666666666666643537020320',
                'lat': 34.02,
                'lng': -118.29,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            },
            {
                'travel_time': 14,
                'rating': '4.7',
                'name': 'Walt Disney Concert Hall',
                'time_to_show': '4 : 08 pm to 5 : 09 pm',
                'place_id': 'ChIJ0xG7n03GwoARsDH_OyyMcrM',
                'time_spent': 1,
                'travel_dist': 7.416,
                'no_of_ratings': 3284,
                'images': ['img/data/Los Angeles/sites/ChIJ0xG7n03GwoARsDH_OyyMcrM/1.jpeg', 'img/data/Los Angeles/sites/ChIJ0xG7n03GwoARsDH_OyyMcrM/2.jpeg', 'img/data/Los Angeles/sites/ChIJ0xG7n03GwoARsDH_OyyMcrM/3.jpeg', 'img/data/Los Angeles/sites/ChIJ0xG7n03GwoARsDH_OyyMcrM/4.jpeg'],
                'cost': 10,
                'time': '7.149999999999999980571097069',
                'lat': 34.06,
                'lng': -118.25,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            },
                {
                'travel_time': 11,
                'rating': '4.7',
                'name': 'California Science Center',
                'time_to_show': '5 : 20 pm to 7 : 50 pm',
                'time_spent': 1.5,
                'place_id': 'ChIJ21yHTgjIwoARcrUbrsffOB4',
                'travel_dist': 6.808,
                'no_of_ratings': 5709,
                'images': ['img/data/Los Angeles/sites/ChIJ21yHTgjIwoARcrUbrsffOB4/1.jpeg', 'img/data/Los Angeles/sites/ChIJ21yHTgjIwoARcrUbrsffOB4/2.jpeg', 'img/data/Los Angeles/sites/ChIJ21yHTgjIwoARcrUbrsffOB4/3.jpeg', 'img/data/Los Angeles/sites/ChIJ21yHTgjIwoARcrUbrsffOB4/4.jpeg'],
                'cost': 10,
                'time': '8.333333333333333300951828448',
                'lat': 34.02,
                'lng': -118.29,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }
        ],
        [
            {
                'travel_time': -1,
                'rating': '4.7',
                'name': 'Griffith Park',
                'time_to_show': '9 : 00 am to 10 : 30 am',
                'place_id': 'ChIJ9590IY3AwoARquS6ie60MUc',
                'time_spent': 1.5,
                'travel_dist': -1,
                'no_of_ratings': 19078,
                'images': ['img/data/Los Angeles/sites/ChIJ9590IY3AwoARquS6ie60MUc/1.jpeg', 'img/data/Los Angeles/sites/ChIJ9590IY3AwoARquS6ie60MUc/2.jpeg', 'img/data/Los Angeles/sites/ChIJ9590IY3AwoARquS6ie60MUc/3.jpeg', 'img/data/Los Angeles/sites/ChIJ9590IY3AwoARquS6ie60MUc/4.jpeg'],
                'cost': 10,
                'time': 0,
                'lat': 34.14,
                'lng': -118.29,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }, 
            {
                'travel_time': 25,
                'rating': '4.5',
                'name': 'Hollywood Sign',
                'time_to_show': '10 : 55 am to 11 : 55 am',
                'place_id': 'ChIJfVpQRQq_woARQ5hwJsast6s',
                'time_spent': 1,
                'travel_dist': 12.445,
                'no_of_ratings': 3591,
                'images': ['img/data/Los Angeles/sites/ChIJfVpQRQq_woARQ5hwJsast6s/1.jpeg', 'img/data/Los Angeles/sites/ChIJfVpQRQq_woARQ5hwJsast6s/2.jpeg', 'img/data/Los Angeles/sites/ChIJfVpQRQq_woARQ5hwJsast6s/3.jpeg', 'img/data/Los Angeles/sites/ChIJfVpQRQq_woARQ5hwJsast6s/4.jpeg'],
                'cost': 10,
                'time': '1.916666666666666685170383744',
                'lat': 34.13,
                'lng': -118.32,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }, 
            {
                'travel_time': 17,
                'rating': '4.6',
                'name': 'Hollywood Bowl',
                'time_to_show': '12 : 12 pm to 2 : 42 pm',
                'place_id': 'ChIJMwknwRu_woAR_eI2OM9ib2o',
                'travel_dist': 5.579,
                'no_of_ratings': 6840,
                'time_spent': 2.5,
                'images': ['img/data/Los Angeles/sites/ChIJMwknwRu_woAR_eI2OM9ib2o/1.jpeg', 'img/data/Los Angeles/sites/ChIJMwknwRu_woAR_eI2OM9ib2o/2.jpeg', 'img/data/Los Angeles/sites/ChIJMwknwRu_woAR_eI2OM9ib2o/3.jpeg', 'img/data/Los Angeles/sites/ChIJMwknwRu_woAR_eI2OM9ib2o/4.jpeg'],
                'cost': 10,
                'time': '3.200000000000000011102230246',
                'lat': 34.11,
                'lng': -118.34,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }, 
            {
                'travel_time': 8,
                'rating': '4.7',
                'name': 'Runyon Canyon Park',
                'time_to_show': '2 : 49 pm to 3 : 49 pm',
                'place_id': 'ChIJhX1uVuC-woARQNzq4-b1Prk',
                'travel_dist': 2.346,
                'no_of_ratings': 1638,
                'time_spent': 1,
                'images': ['img/data/Los Angeles/sites/ChIJhX1uVuC-woARQNzq4-b1Prk/1.jpeg', 'img/data/Los Angeles/sites/ChIJhX1uVuC-woARQNzq4-b1Prk/2.jpeg', 'img/data/Los Angeles/sites/ChIJhX1uVuC-woARQNzq4-b1Prk/3.jpeg', 'img/data/Los Angeles/sites/ChIJhX1uVuC-woARQNzq4-b1Prk/4.jpeg'],
                'cost': 10,
                'time': '5.833333333333333342585191872',
                'lat': 34.11,
                'lng': -118.35,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }, 
            {
                'travel_time': 11,
                'rating': '4.7',
                'name': 'Hollywood Pantages Theatre',
                'time_to_show': '4 : 01 pm to 5 : 01 pm',
                'place_id': 'ChIJAye4Ajm_woARztbwsoUDFug',
                'travel_dist': 2.536,
                'time_spent': 1,
                'no_of_ratings': 3068,
                'images': ['img/data/Los Angeles/sites/ChIJAye4Ajm_woARztbwsoUDFug/1.jpeg', 'img/data/Los Angeles/sites/ChIJAye4Ajm_woARztbwsoUDFug/2.jpeg', 'img/data/Los Angeles/sites/ChIJAye4Ajm_woARztbwsoUDFug/3.jpeg', 'img/data/Los Angeles/sites/ChIJAye4Ajm_woARztbwsoUDFug/4.jpeg'],
                'cost': 10,
                'time': '7.016666666666666662965923251',
                'lat': 34.1,
                'lng': -118.33,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }, 
            {
                'travel_time': 16,
                'rating': '4.7',
                'name': 'Griffith Observatory',
                'time_to_show': '5 : 17 pm to 8 : 17 pm',
                'time_spent': 3,
                'place_id': 'ChIJywjU6WG_woAR3NrWwrEH_3M',
                'travel_dist': 6.214,
                'no_of_ratings': 3284,
                'images': ['img/data/Los Angeles/sites/ChIJywjU6WG_woAR3NrWwrEH_3M/1.jpeg', 'img/data/Los Angeles/sites/ChIJywjU6WG_woAR3NrWwrEH_3M/2.jpeg', 'img/data/Los Angeles/sites/ChIJywjU6WG_woAR3NrWwrEH_3M/3.jpeg', 'img/data/Los Angeles/sites/ChIJywjU6WG_woAR3NrWwrEH_3M/4.jpeg'],
                'cost': 10,
                'time': '8.283333333333333325931846502',
                'lat': 34.12,
                'lng': -118.3,
                'rating_len': [0, 1, 2, 3, 4],
                'description': ''
            }
        ]
    ],
    'start_date': '2018-08-22', 
    'no_days': 2
}

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


def itenerary_form(request): 
    form = IteneraryForm()
    if request.method == "POST":
        form = IteneraryForm(request.POST)
        if form.is_valid():
            form.save()
            context = dict()
            context['city']= form.cleaned_data.get("city")
            context['start_date'] = form.cleaned_data.get("start_date")
            context['end_date'] = form.cleaned_data.get("end_date")
            context['type_tags'] = form.cleaned_data.get("type_tags")
            # return HttpResponse('hfggh')
            # global plan
            # plan = add_images_rating(json.loads(generate_itenerary(context)))
            # print "+++++++++++++++++++"
            # print(plan)
            return HttpResponseRedirect('/iteneraryApplication/show_plan/');
    
        # return render(request, 'templates/index2.html', {'form': itene})
    return render(request, 'index2.html', {'form': form})
    # return render(request, html template page to return after form, params for form)

def show_itenerary_list(request):
    global plan
    return render(request, 'show_calender.html', {'plan': json.dumps(plan)})

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

@ensure_csrf_cookie
def update_tour(request):
    plan = request.POST.get('plan', None)
    plan = json.loads(plan)
    event_end = request.POST.get('event_end', None)
    event_start = request.POST.get('event_start', None)
    event_name = request.POST.get('event_name', None)
    # print event_start
    plan = modify_itenerary(plan,event_name,event_start,event_end)
    if plan == -1:
        raise Http404("the change in event is not consistent")
    plan = json.dumps(plan)
    # print plan
    return HttpResponse(plan)

def get_POI_all(request):
    city = request.GET.get('city', None)
    POI_list = get_POIs(city)
    POI_name_list = []
    for POI in POI_list:
       POI_name_list.append(POI.POI_name.encode('ascii','ignore'))
    
    return HttpResponse(json.dumps(POI_name_list))

def get_POI(request):
    POI_name = request.GET.get('POI_name',None)
    POI_city = request.GET.get('POI_city', None)
    POI = get_POI_object(POI_name, POI_city)
    POI = generate_POI_dict(POI)
    return HttpResponse(json.dumps(POI))