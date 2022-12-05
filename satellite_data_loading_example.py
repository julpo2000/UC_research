import pandas as pd
from IPython.display import IFrame
import matplotlib.pyplot as plt
import pydap
import getpass
import xarray as xr
import rioxarray as rxr
import netCDF4
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
import seaborn as sns

file_name1 = "data/S5P_PAL__L2__NO2____20210101T031206_20210101T045336_16681_01_020301_20211112T015828.nc"
file_name2 = "S5P_PAL__L2__NO2____20211101T100047_20211101T114216_20998_02_020301_20211215T122137.nc"
file_name3 = "S5P_PAL__L2__NO2____20210825T011458_20210825T025628_20028_02_020301_20211108T083237.nc"

fire_data_name = "data/S5P_PAL__L2__NO2____20210101T150236_20210101T164406_16688_01_020301_20211112T020118.nc"
fire_data2_name = "data/S5P_PAL__L2__NO2____20210104T172836_20210104T191006_16732_01_020301_20211112T021911.nc"
fire_data3_name = "data/S5P_PAL__L2__NO2____20210101T164406_20210101T182536_16689_01_020301_20211112T020123.nc"


file = netCDF4.Dataset(fire_data3_name, format="NETCDF4")
print(file.groups)
NO_data = file['PRODUCT/nitrogendioxide_tropospheric_column']
lat_data = np.array(file['PRODUCT/latitude'])
long_data = np.array(file['PRODUCT/longitude'])
data_quality = np.array(file['PRODUCT/qa_value'])

NO_data = np.array(NO_data)
# NO_data = NO_data.reshape(long_data.shape).squeeze()
# plt.imshow(NO_data)
# plt.show()

amount_of_data_points = -1
remove_masked_values = True
partial_plot = True
longitude_range = (-85, -75)
latitude_range = (20, 35)

filter_quality = True
minimal_data_quality = 0.75


data = np.array([NO_data.flatten()[:amount_of_data_points], long_data.flatten()[:amount_of_data_points],
                 lat_data.flatten()[:amount_of_data_points], data_quality.flatten()[:amount_of_data_points]]).transpose()
columns = ["NO", "Longitude", "Latitude", "qa"]
data_frame = pd.DataFrame(data=data, columns=columns)

print(data_frame.head())
geometry = [Point(xy) for xy in zip(data_frame["Longitude"], data_frame["Latitude"])]
geo_dataframe = gpd.GeoDataFrame(data_frame, crs={'init': "epsg:4326"}, geometry=geometry)

if filter_quality:
    print("filtering on quality..")
    geo_dataframe = geo_dataframe[geo_dataframe["qa"] >= minimal_data_quality]
if remove_masked_values:
    print("removing masked values..")
    geo_dataframe = geo_dataframe[geo_dataframe["NO"] < 1]
if partial_plot:
    print("removing values outside long/lat range..")
    geo_dataframe = geo_dataframe[geo_dataframe["Longitude"] > longitude_range[0]]
    geo_dataframe = geo_dataframe[geo_dataframe["Longitude"] < longitude_range[1]]
    geo_dataframe = geo_dataframe[geo_dataframe["Latitude"] > latitude_range[0]]
    geo_dataframe = geo_dataframe[geo_dataframe["Latitude"] < latitude_range[1]]

print(geo_dataframe.head())

fig, ax = plt.subplots(1, 1)
geo_dataframe.plot(column="NO", ax=ax, legend=True)
plt.show()


# gebruiken voor data
# rioxarray

# als elke pixel even groot:
# orthorectified
