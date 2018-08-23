from django.conf.urls import url 
from . import views


urlpatterns = [
	# url(r'^/city/add/$', views.add_city, name='add_city'),                     #views.add_city is the function which handles the call and name is used to refer the url elsewhere so that it is not hardcoded
	url(r'^form/$', views.itenerary_form, name='itenerary_form'),
	url(r'^thanks/$', views.thanks, name="thanks"),
	url(r'^show_plan/$', views.show_plan, name="show_plan"),
	url(r'^map/$', views.show_map, name="show_map"),
	url(r'^map_test/$', views.show_map_test, name="show_map_test")
]
