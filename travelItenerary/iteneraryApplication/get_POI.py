from .models import City, PointOfInterest

def get_POIs(city):
	POI_list = PointOfInterest.objects.filter(POI_city = city)
	return POI_list

def get_POI_object(POI_name, city_name):
	POI = PointOfInterest.objects.filter(POI_city = city_name, POI_name = POI_name)
	return POI[0]