from .models import City, Type, PointOfInterest, OpenCloseTime, Photo, Form, DistanceTime
from sklearn.cluster import KMeans
import numpy as np
from tsp_solver import tsp_solver, calculate_time, calculate_time_upto
from .gratification import gratification_score
import json, datetime
from django.core.serializers.json import DjangoJSONEncoder
import math
from .get_POI import get_POI_object

half_day_time = 12

grat_score_dict = dict()

def generate_POI_dict(POI):
	POI_json = dict()
	POI_json['lat'] = float(POI.latitude)
	POI_json['lng'] = float(POI.longitude)
	POI_json['name'] = POI.POI_name
	POI_json['place_id'] = POI.POI_id
	POI_json['rating'] = float(POI.rating)
	POI_json['description'] = POI.description
	POI_json['cost'] = 10
	
	return POI_json

def generate_gratification_score_all(POI_list,form):
	for POI in POI_list:
		grat_score_dict[POI]=gratification_score(POI,form)

def gratification_sort(POI):
	return grat_score_dict[POI]

def tour_sort_key(POI):
	return float(POI['time'])

def generate_itenerary(form):
	city = form['city']
	start_date = form['start_date']
	end_date = form['end_date']

	no_days = (end_date - start_date).days + 1
	POI_list = PointOfInterest.objects.filter(POI_city = city)
	generate_gratification_score_all(POI_list,form)
	kmeans = kMeanClustering(POI_list,no_days)
	
	cluster_list = []

	for i in range(0,no_days):
		cluster_list.append([])

	for i in range(0,len(POI_list)):
		cluster_list[kmeans.labels_[i]].append(POI_list[i])
	
	

	cluster_list = tsp_POI_delegation(cluster_list)
	# print(cluster_list[0])
	output = itenerary_json(cluster_list,form)
	#print(output)
	return output

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
			POI_to_delegate = cluster_list[i].pop(-1)				#removing the last element to fit the time inside half a day
			cluster_list[i+1].append(POI_to_delegate)
			time = calculate_time(cluster_list[i])

	i = no_days-1
	cluster_list[i].sort(key=gratification_sort, reverse=True)
	cluster_list[i] = tsp_solver(cluster_list[i])
	time = calculate_time(cluster_list[i])
	while(time>half_day_time):
			del cluster_list[i][-1]			#removing the last element to fit the time inside half a day
			time = calculate_time(cluster_list[i])

	return cluster_list

def itenerary_json(cluster_list,form):
	json_output={}
	city = form['city']
	start_date = form['start_date']
	end_date = form['end_date']
	no_days = (end_date - start_date).days+1
	tour=[]

	for path in cluster_list:
		path_json = []
		for POI in path:
			POI_json = generate_POI_dict(POI)
			POI_json['time'] = calculate_time_upto(POI,path)
			path_json.append(POI_json)
		tour.append(path_json)
		# print(path)

	json_output['city'] = city.city_name
	json_output['start_date'] = start_date
	json_output['no_days'] = no_days
	json_output['tour'] = tour
	# print(json_output)
	return json.dumps(json_output,cls=DjangoJSONEncoder)

def time_difference(start_time,end_time):
	output=0;
	output+=(end_time.hour - start_time.hour)
	output+=(end_time.minute - start_time.minute)/60.0
	return output

def POI_time(time):
	output = 0;
	output+=(time.hour - 9.0)
	output+=time.minute/60.0
	return float(output)


def modify_itenerary(tour,event_name,event_start,event_end):
	start_day = datetime.datetime.strptime(tour['start_date'], "%Y-%m-%d").date()
	# print tour
	if not check_itenerary_consistency(tour,event_name,event_start,event_end):
		return -1
	POI_is_present = False
	for i in range(0, len(tour['tour'])):
		path = tour['tour'][i]
		for POI in path:
			if POI['name']==event_name:
				
				POI_is_present = True
				start_time = event_start.split("T")[1]
				start_time = start_time.split("+")[0]
				start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
				date_travel = event_start.split("T")[0]
				date_travel = datetime.datetime.strptime(date_travel, "%Y-%m-%d").date()
				end_time = event_end.split("T")[1]
				end_time = end_time.split("+")[0]
				end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
				time_diff = time_difference(start_time,end_time)
				# print time_diff
				POI['time_spent'] = time_diff
				# print POI['time']
				POI['time'] = POI_time(start_time)
				# print POI['time']

				if (date_travel - start_day).days != i:
					path.remove(POI)
					tour['tour'][(date_travel - start_day).days].append(POI)

	if not POI_is_present:
		print event_name
		POI_object = get_POI_object(event_name, tour['city'])
		POI_obj_json = generate_POI_dict(POI_object)
		print POI_object
		start_time = event_start.split("T")[1]
		start_time = start_time.split("+")[0]
		start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
		date_travel = event_start.split("T")[0]
		date_travel = datetime.datetime.strptime(date_travel, "%Y-%m-%d").date()
		end_time = event_end.split("T")[1]
		end_time = end_time.split("+")[0]
		end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
		time_diff = time_difference(start_time,end_time)
		# print time_diff
		POI_obj_json['time_spent'] = time_diff
		# print POI['time']
		POI_obj_json['time'] = float(start_time.hour + start_time.minute/60.0 - 9.0)
		# print POI['time']
		tour['tour'][(date_travel - start_day).days].append(POI_obj_json)

	for path in tour['tour']:
		path.sort(key=tour_sort_key)

	for path in tour['tour']:
		for i in range(0, len(path)):
			if i==0:
				path[i]['travel_time'] = 0;
			else:
				timeDiff = float(path[i]['time']) - float(path[i-1]['time']) - path[i-1]['time_spent']
				path[i]['travel_time'] = math.floor(timeDiff*60)

	return tour

def get_actual_time_difference(POI_first, POI_second, city_name):
	POI_source = PointOfInterest.objects.filter(POI_city = city_name, POI_name = POI_first)
	POI_dest = PointOfInterest.objects.filter(POI_city = city_name, POI_name = POI_second)
	# print POI_source
	Distance_time_object = DistanceTime.objects.filter(source = POI_source[0], dest = POI_dest[0])
	time_diff = Distance_time_object[0].time
	return float(time_diff)/60.0
	# return 0


def check_itenerary_consistency(tour,event_name,event_start,event_end):
	start_day = datetime.datetime.strptime(tour['start_date'], "%Y-%m-%d").date()
	# POI = get_POI_object(event_name,tour['city'])

	for path_index in range(0,len(tour['tour'])):
		path = tour['tour'][path_index]
		for POI in path:
			if POI['name'] == event_name:
				continue;
			date_travel = event_start.split("T")[0]
			date_travel = datetime.datetime.strptime(date_travel, "%Y-%m-%d").date()
			if((date_travel - start_day).days > path_index):
				break;
			if((date_travel - start_day).days < path_index):
				return True
			start_time_event = event_start.split("T")[1]
			start_time_event = start_time_event.split("+")[0]
			start_time_event = datetime.datetime.strptime(start_time_event, '%H:%M:%S').time()
			end_time_event= event_end.split("T")[1]
			end_time_event = end_time_event.split("+")[0]
			end_time_event = datetime.datetime.strptime(end_time_event, '%H:%M:%S').time()

			POI_event_start_time = POI_time(start_time_event)
			POI_event_end_time = POI_time(end_time_event)
			POI_end_time = float(POI['time']) + float(POI['time_spent'])
			POI_start_time = float(POI['time'])
			if POI_event_start_time == POI_start_time or POI_event_end_time == POI_end_time:
				return False
			if POI_event_start_time < POI_start_time:
				if POI_event_end_time > POI_start_time:
					return False
				travel_time = POI_start_time - POI_event_end_time
				# print travel_time
				# print "<><><><<><><><><><<><><><><><><><><><><><><><><><><><><>"
				travel_time_actual = get_actual_time_difference(event_name,POI['name'],tour['city'])
				if travel_time >= travel_time_actual:
					return True
				return False

			if POI_start_time < POI_event_start_time:
				if POI_end_time > POI_event_start_time:
					return False
				travel_time = POI_event_start_time - POI_end_time
				travel_time_actual = get_actual_time_difference(POI['name'],event_name,tour['city'])
				if travel_time >= travel_time_actual:
					return True
				return False

	return True			


