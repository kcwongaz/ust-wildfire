from ust_wildfire.wildfire_stat import *

import numpy as np
import pandas as pd
import sys


label = sys.argv[1]
fname = "../data/{label}.csv"

year_min = 1950
year_max = 2021
years = np.arange(year_min, year_max + 1)
months = np.arange(1, 13)


# To reproduce the result of Prof. Li's 2013 paper
repeat2013 = False

# Filter events that span across multiple months
# This will ignore events with no end-date data
no_cross_month = False


# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
df = filter_year(df, year_min, year_max)

if repeat2013:
    df = filter_repeat2013(df)


yr_stat = wildfire_stat_yearly(df, years)
mo_stat = wildfire_stat_monthly(df, months, no_cross_month)

yr_stat.to_csv(f"../data/results/{label}_yearly_stat.csv", index=False)
yr_stat.to_csv(f"../data/results/{label}_monthly_stat.csv", index=False)
