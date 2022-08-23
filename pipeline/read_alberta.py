import pandas as pd
import numpy as np


def read_alberta1961(fname):

    df = pd.read_csv(fname, header=0)
    df = df.dropna(subset=["YEAR", "MON", "DAY"])  # Drop rows without date

    timecolumns = zip(df["YEAR"], df["MON"], df["DAY"], df["HRSTART"])
    timestamp = [get_timestamp_alberta1961(*x) for x in timecolumns]

    df = df[["LAT", "LONG", "TOTAL"]]
    df = df.rename(columns={"LAT": "lat",
                            "LONG": "lon",
                            "TOTAL": "size"})
    df = df.assign(start_time=timestamp)
    df = df.assign(end_time=np.nan)

    # Convert acres to ha
    df["size"] = df["size"] * 0.40468564

    return df


def get_timestamp_alberta1961(year, month, day, time):

    year = 1900 + int(year)
    month = int(month)
    day = int(day)
    hour = int(time // 10)
    minu = int(time % 10 * 6)

    if year < 61:
        print("1961 wrong year!")

    # Make sure day is correct
    if day == 0:
        day = 1

    if month in (1, 3, 5, 7, 8, 10, 12) and day > 31:
        day = 31
    elif month in (4, 6, 9, 11) and day > 30:
        day = 30
    elif month == 2 and day > 29:
        day = 28

    # Make sure hour is correct
    if hour > 23:
        hour = 0

    ts = int(pd.Timestamp(year=year, month=month, day=day,
                          hour=hour, minute=minu).timestamp())

    return ts


def read_alberta1983(fname):

    # This may give a DtypeWarning ... should not be a problem
    df = pd.read_csv(fname, header=0)
    df = df.dropna(subset=["starttime", "startdate"])  # Drop rows without date

    start_time = [get_timestamp_alberta1983(*x) for x in zip(df["startdate"], df["starttime"])]
    end_time = [get_timestamp_alberta1983(*x) for x in zip(df["extingdate"], df["extingtime"])]

    df = df[["lat", "long", "extingsize"]]
    df = df.rename(columns={"long": "lon", "extingsize": "size"})
    df = df.assign(start_time=start_time)
    df = df.assign(end_time=end_time)

    return df


def get_timestamp_alberta1983(date, time):

    if pd.isna(date) or pd.isna(time):
        return np.nan

    # Internally, pandas read the date in format YYYY-MM-DD
    d = date.split("-")

    if time > 2359:
        time = 0

    hour = int(time // 100)
    minu = int(time % 100)

    if hour > 23:
        hour = 0
    if minu > 59:
        minu = 0

    ts = int(pd.Timestamp(year=int(d[0]), month=int(d[1]), day=int(d[2]),
                          hour=hour, minute=minu).timestamp())

    return ts


def read_alberta1996(fname):

    df = pd.read_csv(fname, header=0)

    # Drop rows with no or wrong start date
    df = df.dropna(subset=["fire_start_date"])
    df = df.loc[df["fire_start_date"].str[:4].astype(int) >= 1996]

    start_time = [get_timestamp_alberta1996(x) for x in df["fire_start_date"]]
    end_time = [get_timestamp_alberta1996(x) for x in df["ex_fs_date"]]

    df = df[["fire_location_latitude", "fire_location_longitude", "current_size"]]
    df = df.rename(columns={"fire_location_latitude": "lat",
                            "fire_location_longitude": "lon",
                            "current_size": "size"})

    df = df.assign(start_time=start_time)
    df = df.assign(end_time=end_time)

    return df


def read_alberta2006(fname):

    # Alberta 2006-2018 file does not use UTF-8
    df = pd.read_csv(fname, header=0, encoding="cp1252")

    # Drop rows with no or wrong start date
    df = df.dropna(subset=["fire_start_date"])
    df = df.loc[df["fire_start_date"].str[:4].astype(int) >= 2006]

    start_time = [get_timestamp_alberta1996(x) for x in df["fire_start_date"]]
    end_time = [get_timestamp_alberta1996(x) for x in df["ex_fs_date"]]

    df = df[["fire_location_latitude", "fire_location_longitude", "current_size"]]
    df = df.rename(columns={"fire_location_latitude": "lat",
                            "fire_location_longitude": "lon",
                            "current_size": "size"})

    df = df.assign(start_time=start_time)
    df = df.assign(end_time=end_time)

    return df


def get_timestamp_alberta1996(tstr):

    if pd.isna(tstr):
        return np.nan

    fmt = "%Y-%m-%d %H:%M"
    t = int(pd.to_datetime(tstr, format=fmt).timestamp())

    return t


def add_year_month(df):
    timestamps = [pd.Timestamp(t, unit="s") for t in df["start_time"]]
    months = [ts.month for ts in timestamps]
    years = [ts.year for ts in timestamps]

    df = df.assign(year=years)
    df = df.assign(month=months)

    return df


# ---------------------------------------------------------------------------- #
frames = [read_alberta1961("../raw/alberta_1961_1982.csv"),
          read_alberta1983("../raw/alberta_1983_1995.csv"),
          read_alberta1996("../raw/alberta_1996_2005.csv"),
          read_alberta2006("../raw/alberta_2006_2018.csv")]

dataframe = pd.concat(frames)
dataframe = add_year_month(dataframe)

dataframe.to_csv("../data/alberta.csv", index=False)
