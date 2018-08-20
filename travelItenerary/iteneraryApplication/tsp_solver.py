from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
from .models import Distance

def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

	def distance_callback(from_node, to_node):
		return int(dist_matrix[from_node][to_node])

	return distance_callback

def create_distance_matrix(POI_list):
	dist_matrix = np.zeros(no_POI,no_POI)
	for i in range(0,len(POI_list)):
		for j in range(0,len(POI_list)):
			if i==j:
				dist_matrix[i][j] = 0
			else:
				distance_i_to_j_object = Distance.objects.filter(source = POI_list[i], dest = POI_list[j])
				dist_matrix[i][j] = distance_i_to_j_object.distance
	return dist_matrix



def tsp_solver(POI_list):

	tsp_size = len(POI_list)
	num_routes = 1
	depot = 0
	dist_matrix = create_distance_matrix(POI_list)
	route = []


	# Create routing model
	if tsp_size > 0:
	routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
		search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
		# Create the distance callback.
		dist_callback = create_distance_callback(dist_matrix)
    	routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
		# Solve the problem.
		assignment = routing.SolveWithParameters(search_parameters)
		if assignment:
	    	# Solution distance.
	    	print "Total distance: " + str(assignment.ObjectiveValue()) + " miles\n"
	    	# Display the solution.
	    	# Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
	    	route_number = 0
	    	index = routing.Start(route_number) # Index of the variable for the starting node.

	    	while not routing.IsEnd(index):
	     		# Convert variable indices to node indices in the displayed route.
	    		route.append(POI_list[routing.IndexToNode(index)])
	    		index = assignment.Value(routing.NextVar(index))
	    	route.append(POI_list[routing.IndexToNode(index)])
	    	print "route calculated"
		else:
			print 'No solution found.'
	else:
		print 'Specify an instance greater than 0.'
	
	return route
