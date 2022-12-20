import matplotlib.pyplot as plt
import netCDF4
import numpy as np

from blob_detection import plume_mask
from morans_i import morans_i
from total_NO2_calculations import calculate_no2_in_plume

# download data from https://data-portal.s5p-pal.com/browser/BXADeFDHwTQ3o8nrrhTDZSMwnfrWHe16d/2JM1fiAU7vaLzQZSRP3o4uRznddN4VH4NGpp4dfkKSnZV4hzrZifph

fire_1 = {"file": "data/S5P_PAL__L2__NO2____20210831T193807_20210831T211937_20124_02_020301_20211108T091419.nc", "point_of_interest" : (39.9901 -120.5113)}
fire_2 = {"file": "data/S5P_PAL__L2__NO2____20210723T201253_20210723T215423_19571_02_020301_20211107T190856.nc", "point_of_interest" : (40.0246,-120.9138)}
fire_3 = {"file": "data/S5P_PAL__L2__NO2____20210803T200552_20210803T214721_19727_02_020301_20211108T061938.nc", "point_of_interest" : (40.7763,-123.3876)}
fire_4 = {"file": "data/S5P_PAL__L2__NO2____20210620T185122_20210620T203252_19102_01_020301_20211107T155510.nc", "point_of_interest" : (39.7297,-108.8945)}
fire_5 = {"file": "data/S5P_PAL__L2__NO2____20210907T190542_20210907T204711_20223_02_020301_20211108T095642.nc", "point_of_interest" : (41.6047,-121.7298)}

choosen_fire=fire_5

file = netCDF4.Dataset(choosen_fire["file"], format="NETCDF4")
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
point_of_interest = choosen_fire["point_of_interest"]
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


fig, axs = plt.subplots(2, 2)
axs[0, 0].set_title("Raw NO data")
axs[0, 0].imshow(NO_data_sliced)

morans_i = morans_i(NO_data_sliced)
axs[0, 1].set_title("Local Morans I")
axs[0, 1].imshow(morans_i)

plume_mask = plume_mask(morans_i, sensitivity=2)
axs[1, 0].set_title("Plume Mask")
axs[1, 0].imshow(plume_mask)

result = calculate_no2_in_plume(plume_mask*NO_data_sliced)
print(f"Total NO2 in KG: {result}")
axs[1, 1].set_title(f"NO2 in Plume: {int(result)} KG")
axs[1, 1].imshow(plume_mask*NO_data_sliced)

plt.show()




