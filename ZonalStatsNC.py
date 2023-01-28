import xarray as xr
import rasterio as rio
import geopandas as gpd
import rasterstats as rstats
import pandas as pd
import warnings
import numpy as np
import csv
import time as timerr

warnings.filterwarnings('ignore')

# load and read shp-file with geopandas
shp_fo = "C:\\Users\\BerkayAkpinar\\Desktop\\ISMIP\\TR\\LocationsGridsForStats\\ZonalStatGrids.shp"
shp_df = gpd.read_file(shp_fo)

# load and read netCDF-file to dataset and get datarray for variable
nc_fo = "C:\\Users\\BerkayAkpinar\\Desktop\\ERA5LAND_TR\\ALL_DAILY_DATA\\TempDaily\\ERA5LAND_TR_TEMP_DAILY_ALL_79-2014.nc"

nc_ds = xr.open_dataset(nc_fo)
nc_var = nc_ds['t2m']

# ID = shp_df['ID']
ID = shp_df[shp_df['ID'] < 1000] # we can select interval of ID if needed
ID = ID.ID

# get all years for which we have data in nc-file
times = nc_ds['time'].values

# get affine of nc-file with rasterio
affine = rio.open(nc_fo).transform

start = timerr.perf_counter()


for j in ID:
    # go through all years
    # timer
    start_time = timerr.time()
    final_data = pd.DataFrame(columns=['date', 'ID', 'MedianTas'])
    for time in times:

            # get values of variable pear year
            nc_arr = nc_var.sel(time=time)
            nc_arr_vals = nc_arr.values

            #go through all geometries and compute zonal statistics

            a = rstats.zonal_stats(shp_df.geometry[shp_df.ID == j], nc_arr_vals, affine=affine, stats="median")

            #final_data.append(mylist)

            date_to_write= pd.to_datetime(time)

            final_data =final_data.append({'date': date_to_write,
                                              'ID': j,
                                              'MedianTas': a},
                                              ignore_index = True)

    end_time = timerr.time()
    time_dif = start_time - end_time
    final_data.to_csv('C:\\Users\\BerkayAkpinar\\Desktop\\ISMIP\\TR\\LocationsGridsForStats\\Daily\\ZonalStatGridsDailyERA'+str(j)+'.csv')
    print('ID ' + str(j) + ' done' + ' in' + str(time_dif) + ' seconds')






