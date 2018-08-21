from .models import PointOfInterest, Type, Form
import scipy.stats as st
import math

not_matching_score = 100
matching_score = 10000

def p_mean(rating):
	return float((rating - 1)/4)

def calc_popularity(POI):
	z_score = st.norm.ppf(0.975)
	p = p_mean(POI.rating)
	n = POI.no_people_who_rated
	lower_bound = p+(z_score*z_score)/(2*n)
	lower_bound -=z_score*math.sqrt((p*(1-p) + z_score*z_score/(4*n))/n)
	lower_bound/=(1+z_score*z_score/n)

	return lower_bound

def gratification_score(POI,form):
	POI_types = POI.types.all()
	form_types = form['type_tags']

	grat_score = 0
	for type in form_types:
		if type in POI_types:
			grat_score+=matching_score
		else:
			grat_score+=not_matching_score

	grat_score = math.log(grat_score)*calc_popularity(POI)
	return grat_score