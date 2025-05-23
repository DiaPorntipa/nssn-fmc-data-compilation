import calendar
import os
import subprocess
import urllib
import urllib.request
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr
from scipy.constants import convert_temperature


def get_barra2_grid_point():
    # Download one barra2 file to extract grid cells
    url = "https://thredds.nci.org.au/thredds/fileServer/ob53/output/reanalysis/AUST-04/BOM/ERA5/historical/hres/BARRA-C2/v1/1hr/tas/latest/tas_AUST-04_ERA5_historical_hres_BOM_BARRA-C2_v1_1hr_201812-201812.nc"
    sampled_barra2_file_path = os.path.join("..", "Data", "barra2_tas_201812.nc")
    if not os.path.exists(sampled_barra2_file_path):
        urllib.request.urlretrieve(url, sampled_barra2_file_path)

    ds = xr.open_dataset(sampled_barra2_file_path)

    lats = ds["lat"].values
    lons = ds["lon"].values

    return lats, lons


def find_nearest_barra2_grid_point(x, y, lon_grid, lat_grid):
    nearest_lon = lon_grid[np.abs(lon_grid - x).argmin()]
    nearest_lat = lat_grid[np.abs(lat_grid - y).argmin()]
    return nearest_lon, nearest_lat


def download_all_barra2_data(vars, barra2_cell_locations_list, first_datetime, last_datetime):
    barra2_data_dir = os.path.join("..", "Data", "barra2")
    os.makedirs(barra2_data_dir, exist_ok=True)

    for i, (x, y) in enumerate(barra2_cell_locations_list):
        print(f"Downloading data for barra2 cell coordinate {i + 1} of {len(barra2_cell_locations_list)}")
        current_dt = first_datetime.replace(day=1)

        while current_dt <= last_datetime:
            year = current_dt.year
            month = current_dt.month
            yyyymm = f"{year}{month:02d}"

            # Determine time_start and time_end for this month
            month_start = current_dt
            last_day = calendar.monthrange(year, month)[1]
            month_end = datetime(year, month, last_day)

            raw_start = month_start.strftime("%Y-%m-%dT00:00:00Z")
            raw_end = month_end.strftime("%Y-%m-%dT23:00:00Z")
            time_start = urllib.parse.quote(raw_start, safe="")
            time_end = urllib.parse.quote(raw_end, safe="")

            # Download temperature and relative humidity data
            for var in vars:
                url = f"https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUST-04/BOM/ERA5/historical/hres/BARRA-C2/v1/1hr/{var}/latest/{var}_AUST-04_ERA5_historical_hres_BOM_BARRA-C2_v1_1hr_{yyyymm}-{yyyymm}.nc?var={var}&latitude={y}&longitude={x}&time_start={time_start}&time_end={time_end}&timeStride=&vertCoord=&accept=csv"
                output_file_path = os.path.join(barra2_data_dir, f"barra2_data_{var}_{x}_{y}_{yyyymm}.csv")
                print(f"Downloading {output_file_path} from {url}")
                subprocess.run(["curl", "-s", "-L", "-C", "-", "-o", output_file_path, url])

            # Go to next month
            if month == 12:
                current_dt = datetime(year + 1, 1, 1)
            else:
                current_dt = datetime(year, month + 1, 1)


def get_barra2_value(row, var):
    yyyymm = row["UTC_Datetime"].round("h").strftime("%Y%m")
    file_path = os.path.join("..", "Data", "barra2", f"barra2_data_{var}_{row['barra2_X']}_{row['barra2_Y']}_{yyyymm}.csv")
    df_barra2 = pd.read_csv(file_path)

    target_time = row["UTC_Datetime"].round("h").strftime("%Y-%m-%dT%H:%M:%SZ")
    column_name = df_barra2.columns[df_barra2.columns.str.contains(var)]
    barra2_value = df_barra2.loc[df_barra2["time"] == target_time, column_name].values[0][0]
    if var == "tas":
        barra2_value = convert_temperature(barra2_value, "Kelvin", "Celsius")

    return barra2_value
