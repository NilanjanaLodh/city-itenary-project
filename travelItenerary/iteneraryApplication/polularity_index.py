from .models import PointOfInterest
import scipy.stats as st


def calc_popularity(POI):
	z-score = st.norm.ppf(0.975)

	