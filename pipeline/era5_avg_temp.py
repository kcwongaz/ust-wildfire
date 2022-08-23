from ust_wildfire.era5 import *

import numpy as np
import sys
from netCDF4 import Dataset


label = sys.argv[1]
ncdir = f"../data/era5_{label}"
outname = f"../data/{label}_hourly_temp.csv"

yr_start = 1950
yr_end = 2019

# --------------------------------------------------------------------------- #
all_temp = np.array([])

for yr in range(yr_start, yr_end+1):
    print(f"... Now working on {yr}")

    # Data from current year
    nc = Dataset(f"{ncdir}/{label}_{yr}.nc", "r")
    t2m1 = nc.variables["t2m"][:,:,:] - 273.15
    
    avg = np.average(t2m1, axis=(1, 2))
    all_temp = np.concatenate((all_temp, avg))

np.savetxt(outname, all_temp)
