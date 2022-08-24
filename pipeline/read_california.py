import pandas as pd
import numpy as np
import json


def read_california(fname):

    to_df = {"lat": [],
            "lon": [],
            "size": [],
            "start_time": [],
            "end_time": [],
            "year": [],
            "month": []}

    with open(fname) as f:
        data = json.load(f)["features"]

        for row in data:
            prop = row["properties"]

            # Skip all together if it has no year information
            if not prop["YEAR_"]:
                continue

            to_df["year"].append(prop["YEAR_"])
            to_df["start_time"].append(get_timestamp_california(prop["ALARM_DATE"]))
            to_df["end_time"].append(get_timestamp_california(prop["CONT_DATE"]))

            to_df["month"].append(pd.Timestamp(to_df["start_time"][-1],
                                            unit="s").month)

            # GIS_ACRES can be null, which will give TypeError
            try:
                to_df["size"].append(0.40468564 * prop["GIS_ACRES"])
            except TypeError:
                to_df["size"].append(np.nan)

            # Mean lat, lon
            coord = np.array(flatten_coord(row["geometry"]["coordinates"]))
            lon, lat = np.average(coord, axis=0)

            to_df["lat"].append(lat)
            to_df["lon"].append(lon)

        df = pd.DataFrame(to_df)
        return df


def get_timestamp_california(tstr):

    if pd.isna(tstr):
        return np.nan

    # Known problems
    wrong_years = {"0202": "2020", "1089": "1989",
                   "0209": "2009", "0219": "2019"}

    # Fix wrong year "0202-%m-%d"
    if tstr[:4] in wrong_years:
        tstr = wrong_years[tstr[:4]] + tstr[4:]

    fmt = "%Y-%m-%dT%H:%M:%SZ"
    t = int(pd.to_datetime(tstr, format=fmt).timestamp())

    return t


def flatten_coord(nested_list):
    coordinates = []

    for sublist in nested_list:
        if is_coord(sublist):
            coordinates.append(sublist)
        else:
            coordinates.extend(flatten_coord(sublist))

    return coordinates


def is_coord(arr):
    if len(arr) != 2:
        return False

    if isinstance(arr[0], float) and isinstance(arr[1], float):
        return True
    else:
        return False


# --------------------------------------------------------------------------- #
fname = "../data/raw/california_1950.geojson"
sname = "../data/california.csv"

df = read_california(fname)
df.to_csv(sname, index=False)
