import numpy as np
import pandas as pd


def filter_year(df, year_min, year_max):
    """
    Filter out data not in the desired range
    """

    df = df.loc[(df["year"] >= year_min) &
                (df["year"] <= year_max)]

    return df


def filter_valid_time(df, start=True, end=True):
    """
    Filter out data with no valid start and/or end time
    """

    if start:
        df = df.dropna(subset=["start_time"])

    if end:
        df = df.dropna(subset=["end_time"])

    return df


def filter_repeat2013(df):
    """
    Reproduce the selection of wildfires analyzed by Prof. Li's 2013 paper.
    In that paper, fires in Alberta from 1983 to 2010 are analyzed.
    Extraordinarily large fires of size >50000 ha are excluded.
    """

    df = df.loc[(df["year"] <= 2010) & (df["year"] >= 1983) &
                (df["size"] < 50000)]

    return df


def filter_lifetime(df, cutoff):
    """
    Filter out those wildfires with lifetime = end_time - start_time > cutoff.
    Will keep rows without end_time (so that lifetime is undefined)
    """

    lifetime = (df["end_time"] - df["start_time"]).to_numpy()
    lifetime = lifetime / 86400

    # Index by negation to keep rows with nan lifetime
    df = df.iloc[np.where(~(lifetime > cutoff))]

    return df


def filter_cross_month(df):
    """
    Filter out wildfires that lasted more than one month.
    """

    # Compute end-year and end-month
    end_time = pd.to_datetime(df["end_time"], unit="s")
    df = df.assign(end_month=end_time.dt.month)
    df = df.assign(end_year=end_time.dt.year)

    # Give an extra one-month margin to not overkill
    df = df.loc[(df["end_year"] - df["year"] < 1) &
                (df["end_month"] - df["month"] < 2)]

    return df


def wildfire_stat_yearly(df, years):
    
    area = np.zeros(len(years))
    count = np.zeros(len(years))

    for i, y in enumerate(years):
        df_y = df.loc[df["year"] == y]
        df_y = df_y.dropna(subset=["size"])
        count[i] = len(df_y)

        if len(df_y) == 0:
            area[i] = np.nan
        else:
            area[i] = np.average(df_y["size"])

    df = pd.DataFrame({"year": years, "count": count, "avg_size": area})
    return df


def wildfire_stat_monthly(df, months, no_cross_month):

    if no_cross_month:
        df = filter_cross_month(df)

    area = np.zeros(len(months))
    count = np.zeros(len(months))

    for i, m in enumerate(months):
        df_m = df.loc[df["month"] == m]
        df_m = df_m.dropna(subset=["size"])
        count[i] = len(df_m)

        if len(df_m) == 0:
            area[i] = np.nan
        else:
            area[i] = np.average(df_m["size"])

    df = pd.DataFrame({"month": months, "count": count, "avg_size": area})
    return df
