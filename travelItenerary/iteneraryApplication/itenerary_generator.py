from .models import City, Type, PointOfInterest, OpenCloseTime, Photo, Form
from sklearn.cluster import KMeans
import numpy as np
from tsp_solver import tsp_solver

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

	for i in range(0,no_days)
	{
		cluster_list[i] = tsp_solver(cluster_list[i])
	}


def kMeanClustering(POI_list,no_days):
	coord_matrix = []
	for POI in POI_list:
		latitude = POI.latitude
		longitude = POI.longitude
		coord_matrix.append([latitude,longitude])
	kmeans = KMeans(n_clusters=no_days, random_state=0).fit(coord_matrix)
	return kmeans