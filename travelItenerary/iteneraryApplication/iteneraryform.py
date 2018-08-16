from django.forms import ModelForm
from .models import Form

class IteneraryForm(ModelForm):
	class Meta:
		model = Form
		fields = ['city','start_date','end_date','type_tags']