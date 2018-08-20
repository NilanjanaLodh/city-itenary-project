# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.template import loader
from .iteneraryform import IteneraryForm
import json

# Create your views here.
plan = {
    "city": "Dubai",
    "start_date": "08/21/2018",
    "days": 2,
    "tour":[
                [
                    {
                        "lat": 25.242992, 
                        "lng": 55.33269 ,
                        "name": "Park Hyatt Dubai", 
                        "place_id": "place_id1", 
                        "rating": 5,
                        "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                        "time": "time_to_visit",
                        "cost": "cost"
                    },
                    {
                        "lat": 25.197405, 
                        "lng": 55.274331 ,
                        "name" : "At the top of burj khalifa",
                        "place_id": "place_id2", 
                        "rating": 3,
                        "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                        "time": "time_to_visit",
                        "cost": "cost"

                    },
                    {
                        "name": "The Dubai Mall", 
                        "lat": 25.198518, 
                        "lng": 55.279619,
                        "place_id": "place_id3", 
                        "rating": 4,
                        "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                        "time": "time_to_visit",
                        "cost": "cost"
                    },
                    {
                        "lat": 25.1330986, 
                        "lng": 55.183466 , "name": "Madinat Jumeirah",
                        "place_id": "place_id4", 
                        "rating": 4,
                        "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                        "time": "time_to_visit",
                        "cost": "cost"
                    }
                ],
                [
                    {
                        "lat": 25.139409, 
                        "lng": 55.188844 , 
                        "name": "Wild wadi waterpark",
                        "place_id": "place_id5", 
                        "rating": 5,
                        "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                        "time": "time_to_visit",
                        "cost": "cost"
                    },
                    {
                        "lat": 25.1971411, 
                        "lng": 55.2796665 , 
                        "name" : "Dubai ice rink",
                        "place_id": "place_id6", 
                        "rating": 2,
                        "description": "Lorem ipsum dictumst habitant hendrerit massa nostra fermentum feugiat",
                        "time": "time_to_visit",
                        "cost": "cost"
                    }
                ]
    ]
}


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

    for day in plan['tour']:
        for place in day:
            try:
                place['rating'] = range(place['rating'])
            except:
                pass
    return HttpResponse(loader.get_template("show_plan.html").render(plan))

def thanks(request):
	return HttpResponse("Hello World")

def show_map(request):
    tour = plan["tour"]
    return render(request , 'map.html' , {
        'plan' : json.dumps(tour),
        'start_date' : plan['start_date'], #mm/dd/yy
        'city' : plan['city']
    });