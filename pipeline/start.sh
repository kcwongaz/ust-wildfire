#!/bin/bash

# Before running this script, please confirms you have all the necessary data:
# (1) the raw data sets and (2) the ERA5 data in .nc format sorted by year
# Also ensure that they have the file name assumed by the read_xxx.py scripts

BASEDIR=$(dirname "$BASH_SOURCE")
cd $BASEDIR
echo "Start..."

# Step 1
# Read the wildfire data out from the raw format
# The raw data should be placed in data/raw/, and are assumed to have names
# california_1950.geojson
# alberta_1961_1982.csv, alberta_1983_1995.csv, alberta_1996_2005.csv, alberta_2006_2018.csv
echo "Step 1: Reading wildfire raw data..."
python3 read_california.py
python3 read_alberta.py


# Step 2
# Compute some basic statistics from the wildfire datasets
echo "Step 2: Computing wildfire statistics..."
python3 compute_wildfire_stat.py california
python3 compute_wildfire_stat.py alberta


# Step 3
# Add in the temperature columns to the dataframes
echo "Step 3: Fetching ERA5 temperature data..."
python3 era5_fetch_temp.py california
python3 era5_fetch_temp.py alberta


echo "Done!"
