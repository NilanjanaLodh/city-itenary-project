from django.conf.urls import url 
from . import views


urlpatterns = [
	# url(r'^/city/add/$', views.add_city, name='add_city'),                     #views.add_city is the function which handles the call and name is used to refer the url elsewhere so that it is not hardcoded
	url(r'^form/$', views.itenerary_form, name='itenerary_form'),
	url(r'^thanks/$', views.thanks, name="thanks"),
	url(r'^show_plan/$', views.show_plan, name="show_plan"),
	url(r'^map/$', views.show_map, name="show_map"),
	url(r'^list/$', views.show_itenerary_list, name="show_list"),
	url(r'^ajax/update_tour/$', views.update_tour, name='update_tour'),
	url(r'^ajax/get_POI_all/$', views.get_POI_all, name='get_POI_all'),
	url(r'^ajax/get_POI/$', views.get_POI, name='get_POI'),

]
