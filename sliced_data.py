import matplotlib.pyplot as plt
import netCDF4
import numpy as np

from blob_detection import plume_mask
from morans_i import morans_i
from total_NO2_calculations import calculate_no2_in_plume

# download data from https://data-portal.s5p-pal.com/browser/BXADeFDHwTQ3o8nrrhTDZSMwnfrWHe16d/2JM1fiAU7vaLzQZSRP3o4uRznddN4VH4NGpp4dfkKSnZV4hzrZifph

fire_data4_nocal = "data/S5P_PAL__L2__NO2____20210820T194529_20210820T212659_19968_02_020301_20211108T080501.nc"
fire_data5_Eldorado_NF = "data/S5P_PAL__L2__NO2____20210830T195715_20210830T213844_20110_02_020301_20211108T090529.nc"
fire_data6_test = "data/S5P_PAL__L2__NO2____20210710T191622_20210710T205752_19386_02_020301_20211107T175245.nc"


file = netCDF4.Dataset(fire_data6_test, format="NETCDF4")
print(file.groups)
NO_data =  np.array(file['PRODUCT/nitrogendioxide_tropospheric_column']).squeeze()
lat_data = np.array(file['PRODUCT/latitude']).squeeze()
long_data = np.array(file['PRODUCT/longitude']).squeeze()
data_quality = np.array(file['PRODUCT/qa_value']).squeeze()


print(NO_data.shape)
print(lat_data.shape)
print(long_data.shape)
print(data_quality.shape)


# goal point: 39.9, -120.70

# point_of_interest = (39.9, -120.7)
point_of_interest = (42.605, -121.1568)
max_error = 0.1
pixel_radius = 15
filter_out_masked_value = True

latitude_mask = (lat_data < (point_of_interest[0] + max_error)) & (lat_data > (point_of_interest[0] - max_error))
longitude_mask = (long_data < (point_of_interest[1] + max_error)) & (long_data > (point_of_interest[1] - max_error))
full_mask = latitude_mask * longitude_mask

result = np.where(full_mask)
print(result)
index_of_interest = (result[0][0], result[1][0])
print(index_of_interest)


NO_data_sliced = NO_data[index_of_interest[0] - pixel_radius: index_of_interest[0] + pixel_radius,
                         index_of_interest[1] - pixel_radius: index_of_interest[1] + pixel_radius]

# masked values are set to 0 instead of 9.97e+36
if filter_out_masked_value:
    NO_data_sliced = NO_data_sliced * (NO_data_sliced < 1)


fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
ax1.set_title("Raw NO data")
ax1.imshow(NO_data_sliced)

morans_i = morans_i(NO_data_sliced)
ax2.set_title("Local Morans I")
ax2.imshow(morans_i)

plume_mask = plume_mask(morans_i, sensitivity=2)
ax3.set_title("Plume Mask")
ax3.imshow(plume_mask)

result = calculate_no2_in_plume(plume_mask*NO_data_sliced)
print(f"Total NO2 in KG: {result}")
ax4.set_title(f"NO2 in Plume: {int(result)} KG")
ax4.imshow(plume_mask*NO_data_sliced)

plt.show()




