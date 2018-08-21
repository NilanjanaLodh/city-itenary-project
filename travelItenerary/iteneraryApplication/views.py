# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.template import loader
from .iteneraryform import IteneraryForm
import json
from .itenerary_generator import generate_itenerary

# Create your views here.
plan = ""

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
            plan = generate_itenerary(context)
            print(plan)
            HttpResponseRedirect('/show_plan/');
    
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
