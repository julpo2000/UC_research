import numpy as np

# https://earthscience.stackexchange.com/questions/19444/how-to-convert-mol-m2-to-total-mass-e-g-gram-kg-etc

# units in Sentinel-5p NO2 dataset are mol m-2
# NO2 has 46gram per mole
# pixel size of 5.5x3.5km = 19,250,000 m2

# multiply Sentinal-5p NO2 data with units [mol m-2] to get [kg] units
multiplication_factor = 46 * 19250000 / 1000


def calculate_no2_in_plume(array: np.array):
    return np.sum(array*multiplication_factor)




