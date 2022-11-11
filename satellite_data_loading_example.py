import pandas as pd
from IPython.display import IFrame
import matplotlib.pyplot as plt
import pydap
import getpass
import xarray as xr
import netCDF4
import numpy as np
file_name1 = "S5P_PAL__L2__NO2____20210101T031206_20210101T045336_16681_01_020301_20211112T015828.nc"
file_name2 = "S5P_PAL__L2__NO2____20211101T100047_20211101T114216_20998_02_020301_20211215T122137.nc"

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


file = netCDF4.Dataset(file_name2, format="NETCDF4")
# print(file)
print(file['PRODUCT/nitrogendioxide_tropospheric_column'])
subset = file['PRODUCT/nitrogendioxide_tropospheric_column']

subset = np.array(subset)

subset = subset.reshape((3735, 450))
plt.imshow(subset)


plt.show()



