import numpy as np
import pandas as pd


def nan_array(length):
    arr = np.empty(length)
    arr[:] = np.nan

    return arr


def ncdf_to_unixtime(time):

    t0 = pd.to_datetime("1900-01-01")
    delta = pd.to_timedelta(time, unit="h")

    t = t0 + delta
    timestamp = t.timestamp()

    return timestamp


def ncdf_to_unixtime_arr(time_arr):

    timearr = [ncdf_to_unixtime(t) for t in time_arr]
    timearr = np.array(timearr)

    return timearr


def check_cross_year(start_time, end_time):

    start_year = pd.to_datetime(start_time, unit="s").year
    end_year = pd.to_datetime(end_time, unit="s").year
    diff = end_year - start_year

    if diff == 0:
        return True
    elif diff > 1:
        print("Warning: Wildfire event with lifespan of >1 year")
        return False
    else:
        return False


def time_ind(t, time):

    dt = np.abs(t - time)
    ind = np.argmin(dt)

    if np.min(dt) > 86400:
        print("Warning: Time difference exceeded 1 day.")

    return ind


def coord_ind(y, x, lat, lon):

    dy = np.abs(y - lat)
    dx = np.abs(x - lon)

    if np.min(dy) > 1 or np.min(dx) > 1:
        print("Warning: Data point probably out of grid.")

    indy = np.argmin(dy)
    indx = np.argmin(dx)

    return indy, indx


def start_value(row, data, lat, lon, time):

    ind1 = time_ind(row["start_time"], time)
    ind2, ind3 = coord_ind(row["lat"], row["lon"], lat, lon)

    value = data[ind1, ind2, ind3]

    return value


def first_nday_avg(row, data, lat, lon, time, n):

    start_day = (row["start_time"] // 86400) * 86400

    # Handle the first day average first, which is always well-defined
    if n == 1:
        start_ind = time_ind(start_day, time)
        end_ind = time_ind(start_day + n * 86400, time)
        lat_ind, lon_ind = coord_ind(row["lat"], row["lon"], lat, lon)

        avg = np.mean(data[start_ind:end_ind + 1, lat_ind, lon_ind])

        return avg

    # If no data for end date, just return the first day average
    if np.isnan(row["end_time"]) and n > 1:
        return first_nday_avg(row, data, lat, lon, time, n=1)

    # If lifetime is shorter than 1 day, return the 1-day average
    # If lifetime is shorter than n days, return the lifetime average
    end_day = (row["end_time"] // 86400) * 86400
    if (end_day - start_day) < 86400:
        return first_nday_avg(row, data, lat, lon, time, n=1)

    if (end_day - start_day) < n*86400:
        return lifetime_avg(row, data, lat, lon, time)

    # Get the needed indices
    start_ind = time_ind(start_day, time)
    end_ind = time_ind(start_day + n*86400, time)
    lat_ind, lon_ind = coord_ind(row["lat"], row["lon"], lat, lon)

    avg = np.mean(data[start_ind:end_ind + 1, lat_ind, lon_ind])

    return avg


def lifetime_avg(row, data, lat, lon, time):

    # If no data for end date, just return the first day average
    # First day average is better than start time value,
    # because for normal data point,
    # the temperature should be averaged over both days and nights
    if np.isnan(row["end_time"]):
        return first_nday_avg(row, data, lat, lon, time, n=1)

    # Get the needed indices
    start_ind = time_ind(row["start_time"], time)
    end_ind = time_ind(row["end_time"], time)
    lat_ind, lon_ind = coord_ind(row["lat"], row["lon"], lat, lon)

    avg = np.mean(data[start_ind:end_ind + 1, lat_ind, lon_ind])

    return avg


def first_nday_avg_cross(row, data1, data2, lat, lon, time1, time2, n):

    # If no data for end date, just return the first day average
    if np.isnan(row["end_time"]) and n > 1:
        return first_nday_avg(row, data1, lat, lon, time1, n=1)

    # Get the start and end day
    start_day = (row["start_time"] // 86400) * 86400
    end_day = (row["end_time"] // 86400) * 86400

    # If lifetime is shorter than 1 day, return the 1-day average
    # If lifetime is shorter than n days, return the lifetime average
    if (end_day - start_day) < 86400:
        return first_nday_avg(row, data1, lat, lon, time1, n=1)

    if (end_day - start_day) < n*86400:
        return lifetime_avg_cross(row, data1, data2, lat, lon, time1, time2)

    # If the first n-day does not cross year
    n_day = start_day + n*86400
    if n_day < time1[-1]:
        return first_nday_avg(row, data1, lat, lon, time1, n)

    # Get the needed indices
    start_ind = time_ind(start_day, time1)
    end_ind = time_ind(n_day, time2)
    lat_ind, lon_ind = coord_ind(row["lat"], row["lon"], lat, lon)

    concatenated = np.concatenate([data1[start_ind:, lat_ind, lon_ind],
                                   data2[:end_ind+1, lat_ind, lon_ind]])
    avg = np.mean(concatenated)

    return avg


def lifetime_avg_cross(row, data1, data2, lat, lon, time1, time2):

    # If no data for end date, just return the first day average
    # First day average is better than start time value,
    # because for normal data point,
    # the temperature should be averaged over both days and nights
    if np.isnan(row["end_time"]):
        return first_nday_avg(row, data1, lat, lon, time1, n=1)

    # Get the needed indices
    start_ind = time_ind(row["start_time"], time1)
    end_ind = time_ind(row["end_time"], time2)
    lat_ind, lon_ind = coord_ind(row["lat"], row["lon"], lat, lon)

    concatenated = np.concatenate([data1[start_ind:, lat_ind, lon_ind],
                                   data2[:end_ind+1, lat_ind, lon_ind]])
    avg = np.mean(concatenated)

    return avg
