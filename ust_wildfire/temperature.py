import numpy as np
import pandas as pd


def average_yearly_temp(df, years=None, months=None):

    if years is None:
        years = pd.unique(df["year"])
    if months is None:
        months = np.arange(1, 13)

    df = df[(df["month"].isin(months))]

    temp = np.zeros(len(years))
    for i, y in enumerate(years):
        df_sub = df.loc[df["year"] == y]
        temp[i] = np.average(df_sub["temp"])

    return temp


def average_monthly_temp(df, years=None, months=None):

    if years is None:
        years = pd.unique(df["year"])
    if months is None:
        months = np.arange(1, 13)

    df = df[(df["year"].isin(years))]

    temp = np.zeros(len(months))
    for i, m in enumerate(months):
        df_sub = df.loc[df["month"] == m]
        temp[i] = np.average(df_sub["temp"])

    return temp


