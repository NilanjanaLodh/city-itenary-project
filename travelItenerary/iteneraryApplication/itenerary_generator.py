from .models import City, Type, PointOfInterest, OpenCloseTime, Photo, Form
from sklearn.cluster import KMeans
import numpy as np
from tsp_solver import tsp_solver, calculate_time, calculate_time_upto
from .gratification import gratification_score
import json

half_day_time = 12*60

grat_score_dict = dict()

def generate_gratification_score_all(POI_list,form):
	for POI in POI_list:
		grat_score_dict[POI]=gratification_score(POI,form)

def gratification_sort(POI):
	return grat_score_dict[POI]

def generate_itenerary(form):
	city = form.city
	start_date = form.start_date
	end_date = form.end_date

	no_days = (end_date - start_date).days
	POI_list = PointOfInterest.objects.filter(POI_city = city)

	kmeans = kMeanClustering(POI_list,no_days)
	cluster_list = np.empty(no_days,0)

	for i in range(0,len(POI_list)):
		cluster_list[kmeans.label_[i]].append(POI_list[i])

	cluster_list = tsp_POI_delegation(cluster_list)
	return cluster_list

def kMeanClustering(POI_list,no_days):
	coord_matrix = []
	for POI in POI_list:
		latitude = POI.latitude
		longitude = POI.longitude
		coord_matrix.append([latitude,longitude])
	kmeans = KMeans(n_clusters=no_days, random_state=0).fit(coord_matrix)
	return kmeans

def tsp_POI_delegation(cluster_list):
	no_days = len(cluster_list)
	for i in range(0,no_days-1):
		cluster_list[i].sort(key=gratification_sort, reverse=True)
		cluster_list[i] = tsp_solver(cluster_list[i])
		time = calculate_time(cluster_list[i])
		while(time>half_day_time):
			POI_to_delegate = cluster_list[i].pop(len(cluster_list[i])-1)				#removing the last element to fit the time inside half a day
			cluster_list[i+1].append(POI_to_delegate)
			time = calculate_time(cluster_list[i])

	i = no_days-1
	cluster_list[i].sort(key=gratification_sort, reverse=True)
	cluster_list[i] = tsp_solver(cluster_list[i])
	time = calculate_time(cluster_list[i])
	while(time>half_day_time):
			del cluster_list[len(cluster_list[i])-1]			#removing the last element to fit the time inside half a day
			# cluster_list[i+1].append(POI_to_delegate)
			time = calculate_time(cluster_list[i])

	return cluster_list

def itenerary_json(cluster_list,form):
	json_output=""
	"city": "Dubai",
    "start_date": "08/21/2018",
    "days": 2,
    city = form.city
	start_date = form.start_date
	end_date = form.end_date
	no_days = (end_date - start_date).days
	tour=[]

	for path in cluster_list:
		path_json = []
		for POI in path:
			POI_json.lat = POI.latitude
			POI_json.lng = POI.longitude
			POI_json.name = POI.POI_name
			POI_json.place_id = POI.POI_id
			POI_json.rating = POI.rating
			POI_json.description = POI.description
			POI_json.time = calculate_time_upto(POI,path)
			POI_cost = 10
			path_json.append(POI_json)
		tour.append(path_json)

	json_output.dump(city)
	json_output.dump(start_date)
	json_output.dump(no_days)
	json_output.dump(tour)

	return json_output
