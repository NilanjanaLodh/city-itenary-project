from django.conf.urls import url 
from . import views


urlpatterns = [
	url(r'^/city/add/$', views.add_city, name='add_city')                     #views.add_city is the function which handles the call and name is used to refer the url elsewhere so that it is not hardcoded
]
