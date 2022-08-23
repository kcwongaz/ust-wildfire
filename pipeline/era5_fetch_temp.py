from ust_wildfire.era5 import *

import numpy as np
import pandas as pd
import sys
from netCDF4 import Dataset


label = sys.argv[1]
fname = f"../data/{label}.csv"
ncdir = f"../data/era5_{label}"

yr_start = 1950
yr_end = 2020

# --------------------------------------------------------------------------- #
# Calculate:
# (1) Temperature at start time,
# (2) Average temperature on start day,
# (3) Average temperature on first n days,
# (4) Average temperature during the entire fire lifetime

df = pd.read_csv(fname)

# Data with no start time is impossible to assign temperature
df = df.dropna(subset=["start_time"])
df = df.reset_index()


# Treat having end_time < start_time as having no end_time data
df.loc[df["end_time"] < df["start_time"], "end_time"] = np.nan


# In the original Cal Fire data set, the year value may be different from
# the actual starting year
df = df.assign(year=pd.to_datetime(df["start_time"], unit="s").dt.year)


temp_st = nan_array(len(df))
temp_1d = nan_array(len(df))
temp_10d = nan_array(len(df))
temp_lt = nan_array(len(df))


for yr in range(yr_start, yr_end+1):
    print(f"... Now working on {yr}")

    # Data from current year
    nc1 = Dataset(f"{ncdir}/{label}_{yr}.nc", "r")
    t2m1 = nc1.variables["t2m"][:,:,:] - 273.15
    lat = nc1.variables["latitude"][:]
    lon = nc1.variables["longitude"][:]
    time1 = ncdf_to_unixtime_arr(nc1.variables["time"][:])

    # Data from next year (to handle cross-year cases)
    nc2 = Dataset(f"{ncdir}/{label}_{yr+1}.nc", "r")
    t2m2 = nc2.variables["t2m"][:,:,:] - 273.15
    time2 = ncdf_to_unixtime_arr(nc2.variables["time"][:])

    # Fill in data year-by-year
    df_yr = df.loc[df["year"] == yr]
    for i, row in df_yr.iterrows():

        temp_st[i] = start_value(row, t2m1, lat, lon, time1)
        temp_1d[i] = first_nday_avg(row, t2m1, lat, lon, time1, n=1)

        if not check_cross_year(row["start_time"], row["end_time"]):
            temp_10d[i] = first_nday_avg(row, t2m1, lat, lon, time1, n=10)
            temp_lt[i] = lifetime_avg(row, t2m1, lat, lon, time1)
        else:
            temp_10d[i] = first_nday_avg_cross(row, t2m1, t2m2, lat, lon,
                                               time1, time2, n=10)
            temp_lt[i] = lifetime_avg_cross(row, t2m1, t2m2, lat, lon,
                                            time1, time2)


# Main loop completed; now add column to dataframe and dump to csv
df["temp_st"] = temp_st
df["temp_1d"] = temp_1d
df["temp_10d"] = temp_10d
df["temp_lt"] = temp_lt

df.to_csv(fname, index=False)
