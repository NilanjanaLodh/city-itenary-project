# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.template import loader
from .iteneraryform import IteneraryForm

# Create your views here.

def itenerary_form(request): 
	form = IteneraryForm()
	if request.method == "POST":
		form = IteneraryForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse('hfggh')
			# return HttpResponseRedirect('/thanks/')
	
		# return render(request, 'templates/index2.html', {'form': itene})
	return render(request, 'index2.html', {'form': form})
	# return render(request, html template page to return after form, params for form)
def thanks(request):
	return HttpResponse("Hello World")