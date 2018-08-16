# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .iteneraryform import IteneraryForm

# Create your views here.

def itenerary_form(request): 
	if request.method == "POST":
		form = IteneraryForm(request.POST)
		if form.is_valid():
			itenerary_item = form.save()
		

	# return render(request, html template page to return after form, params for form)
