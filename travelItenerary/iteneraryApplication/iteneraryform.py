from django.forms import ModelForm
from .models import Form
from django import forms
import datetime

class IteneraryForm(ModelForm):
	class Meta:
		model = Form
		fields = ['city','start_date','end_date','type_tags']
		widgets = {
	      	'type_tags':forms.CheckboxSelectMultiple,
	    	'start_date': forms.SelectDateWidget(empty_label="Nothing"),
	    	'end_date': forms.SelectDateWidget(empty_label="Nothing"),
	    }

	def clean_start_date(self):
		cleaned_data = super(IteneraryForm, self).clean()
		today_date = datetime.date.today()
		start_date = cleaned_data.get("start_date")

		if start_date<today_date:
			raise forms.ValidationError("the start date is too early")

		return start_date

	def clean_end_date(self):
		cleaned_data = super(IteneraryForm, self).clean()
		today_date = datetime.date.today()
		end_date = cleaned_data.get("end_date")

		if end_date<today_date:
			raise forms.ValidationError("the end date is too early")

		return end_date

	def clean(self):
		cleaned_data = super(IteneraryForm, self).clean()
		start_date = self.cleaned_data.get("start_date")
		end_date = cleaned_data.get("end_date")

		if start_date>end_date:
			raise forms.ValidationError("The start date cannot be after end date")

		# if end_date<today_date:
		# 	raise forms.ValidationError("the end date is too early")

		# if start_date > end_date:
		# 	raise forms.ValidationError("the end date can't be before start date")