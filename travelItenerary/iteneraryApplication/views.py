# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.template import loader
from .iteneraryform import IteneraryForm
import json

# Create your views here.

def itenerary_form(request): 
	form = IteneraryForm()
	if request.method == "POST":
		form = IteneraryForm(request.POST)
		if form.is_valid():
			form.save()
			# return HttpResponse('hfggh')
			return HttpResponseRedirect('/iteneraryApplication/show_plan/')
	
		# return render(request, 'templates/index2.html', {'form': itene})
	return render(request, 'index2.html', {'form': form})
	# return render(request, html template page to return after form, params for form)


def show_plan(request):
    #will get the plan from the algorithm
    plan = {
        "city": "city-name",
        "start_date": "start_date",
        "days": 2,
        "tour":[
                    [
                        {
                            "place_id": "place_id",
                            "place": "place_name",
                            "rating": 3,
                            "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                            "time_spend": "amount_of_time_to_spend",
                            "time": "time_to_visit",
                            "latitude": "lat",
                            "longitude": "long",
                            "cost": "cost"
                        },
                        {
                            "place_id": "place_id2",
                            "place": "place_name2",
                            "rating": 5,
                            "description": "place_description2 scmsdk cnmsdk cnsd ksdkc sdmk cdnskcn sdkcnsd kcndskc mdskcn dksc ns",
                            "time_spend": "amount_of_time_to_spend2",
                            "time": "time_to_visit2",
                            "latitude": "lat",
                            "longitude": "long",
                            "cost": "cost2"
                        }
                    ],
                    [
                        {
                            "place_id": "day2_place_id",
                            "place": "day2_place_name",
                            "rating": 4,
                            "description": "day2_place_description  scmsdk cnmsdk cnsd ksdkc sdmk cdnskcn sdkcnsd kcndskc mdskcn dksc ns",
                            "time_spend": "day2_amount_of_time_to_spend",
                            "time": "day2_time_to_visit",
                            "latitude": "lat",
                            "longitude": "long",
                            "cost": "day2_cost"
                        },
                        {
                            "place_id": "day2_place_id2",
                            "place": "day2_place_name2",
                            "rating": 2,
                            "description": "day2_place_description2  scmsdk cnmsdk cnsd ksdkc sdmk cdnskcn sdkcnsd kcndskc mdskcn dksc ns",
                            "time_spend": "day2_amount_of_time_to_spend2",
                            "time": "day2_time_to_visit2",
                            "latitude": "lat",
                            "longitude": "long",
                            "cost": "day2_cost2"
                        }
                    ]
        ]
    }
    for day in plan['tour']:
        for place in day:
            place['rating'] = range(place['rating'])
    return HttpResponse(loader.get_template("show_plan.html").render(plan))

def thanks(request):
	return HttpResponse("Hello World")

def show_map(request):
    plan = [
    [
        {"lat": 25.242992, "lng": 55.33269 , 'name': 'Park Hyatt Dubai'},
        {"lat": 25.197405, "lng": 55.274331 , 'name' : 'At the top of burj khalifa'},
        {"name": "The Dubai Mall", "lat": 25.198518, "lng": 55.279619},
        {"lat": 25.1330986, "lng": 55.183466 , 'name': 'Madinat Jumeirah'}
    ],
    [
        {"lat": 25.139409, "lng": 55.188844 , 'name': 'Wild wadi waterpark'},
        {"lat": 25.1971411, "lng": 55.2796665 , 'name' : 'Dubai ice rink'}
    ]
    ];
    return render(request , 'map.htm' , {
        'plan' : json.dumps(plan),
        'start_date' : '08/21/2018', #mm/dd/yy
        'city' : 'Dubai'
    });