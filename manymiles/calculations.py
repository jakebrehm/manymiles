"""
Performs calculations and operations related to metrics and visualizations.
"""


import calendar
import datetime as dt

import pandas as pd

from . import utilities
from .models import User


def create_record_timeline_df(
    user: User | int,
    lookback: int | None,
) -> pd.DataFrame:
    """Creates the dataframe that is used for the record timeline chart.
    
    Argument `lookback` is the number of days to look back for data. Leaving
    this argument blank will result in the function returning all data.
    """

    # Get all records for the specified user
    columns = ["record_datetime", "mileage"]
    df = utilities.get_all_records_for_user(user)[columns]

    # Extract the datetime and mileage from the most recent record
    most_recent_dt = df["record_datetime"].max()
    most_recent_record = df.loc[df["record_datetime"].idxmax()]["mileage"]
    # Construct a datetime for today at midnight
    today = dt.date.today()
    midnight = dt.datetime.min.time()
    today_at_midnight = dt.datetime.combine(today, midnight)
    # Check to see if there was already a record today
    if today > most_recent_dt.date():
        # Add today's date to the dataframe if it doesn't already exist
        df.loc[len(df)] = {
            "record_datetime": today_at_midnight,
            "mileage": most_recent_record,
        }

    # Get the maximum mileage value for each day
    df.index = df["record_datetime"]
    df = df.groupby(pd.Grouper(freq="D")).max()

    # Back fill any missing dates
    df["mileage"] = df["mileage"].ffill()

    # If a lookback was specified, filter out any undesired data
    if lookback:
        # Determine the starting date to return data from
        threshold = (dt.datetime.now() - dt.timedelta(days=lookback)).date()
        threshold_dt = dt.datetime.combine(threshold, midnight)
        # Filter out values before the threshold date
        df = df[df.index >= threshold_dt]

    # Drop the extra datetime column
    df = df.drop(labels=["record_datetime"], axis=1)

    # Return the fully constructed dataframe
    return df


def create_record_frequency_df(
    user: User | int,
    period: str | None = None,
) -> pd.DataFrame:
    """Creates the dataframe that is used for the count histogram."""

    # Set default values for parameters
    if not period:
        period = "day"

    # Get all records for the specified user
    columns = ["record_datetime", "mileage"]
    df = utilities.get_all_records_for_user(user)[columns]

    # Set the dataframe index to the date of the record
    df.index = pd.to_datetime(df["record_datetime"])

    # Create columns for the appropriate period year, week, number, and name
    df["year"] = df.index.isocalendar().year
    df["week"] = df.index.isocalendar().week
    if period == "month":
        number_range = range(1, 12+1)
        name_from_number = lambda x: calendar.month_name[x]
        df["number"] = pd.to_datetime(df["record_datetime"]).dt.month
        df["name"] = pd.to_datetime(df["record_datetime"]).dt.month_name()
    else:
        number_range = range(7)
        name_from_number = lambda x: calendar.day_name[x]
        df["number"] = pd.to_datetime(df["record_datetime"]).dt.dayofweek
        df["name"] = pd.to_datetime(df["record_datetime"]).dt.day_name()

    # Determine how many records were made for each day
    group_columns = ["year", "week", "number"]
    df = df.groupby(group_columns).size().reset_index(name="count")
    # Determine average and total records for each period
    df = df.groupby(["number"])["count"].agg(
        average="mean",
        count="sum",
    ).reset_index()

    # Fill in any missing days
    df = df.set_index("number")
    df = df.reindex(number_range, fill_value=0)
    df = df.reset_index(names=["number"])
    
    # Ensure that the days are named and in the correct order and return
    df["name"] = df["number"].apply(name_from_number)
    return df.sort_values(by="number", ascending=True)