import pandas as pd
from IPython.display import IFrame
import matplotlib.pyplot as plt
import pydap
import getpass
import xarray as xr
import netCDF4
import numpy as np
file_name1 = "data/S5P_PAL__L2__NO2____20210101T031206_20210101T045336_16681_01_020301_20211112T015828.nc"
file_name2 = "S5P_PAL__L2__NO2____20211101T100047_20211101T114216_20998_02_020301_20211215T122137.nc"
file_name3 = "S5P_PAL__L2__NO2____20210825T011458_20210825T025628_20028_02_020301_20211108T083237.nc"

fire_data_name = "data/S5P_PAL__L2__NO2____20210101T150236_20210101T164406_16688_01_020301_20211112T020118.nc"
# data = xr.open_dataset(file_name2, engine="netcdf4")
#
#
# print(data.info)
#
# print(data.summary)
# #
# # print(data.info)
#
# print(data.coords)
#
# print(data.attrs)
# print(data['PRODUCT'])


file = netCDF4.Dataset(fire_data_name, format="NETCDF4")
# print(file.groups)
# print(file['PRODUCT/nitrogendioxide_tropospheric_column'])
NO_data = file['PRODUCT/nitrogendioxide_tropospheric_column']
lat_data = np.array(file['PRODUCT/latitude'])
long_data = np.array(file['PRODUCT/longitude'])

NO_data = np.array(NO_data)
# print(lat_data)
# # print(NO_data)
# print(lat_data)
print(long_data)
NO_data = NO_data.reshape((4173, 450))


plt.imshow(NO_data)

# plt.show()


# gebruiken voor data
# rioxarray

# als elke pixel even groot:
# orthorectified