"""
Performs calculations and operations related to metrics and visualizations.
"""


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

    # Get the maximum mileage value for each day
    df.index = df["record_datetime"]
    df = df.groupby(pd.Grouper(freq="D")).max()

    # Back fill any missing dates
    df["mileage"] = df["mileage"].ffill()

    # If a lookback was specified, filter out any undesired data
    if lookback:
        # Determine the starting date to return data from
        most_recent_record = utilities.get_most_recent_record(user)
        threshold = most_recent_record.record_datetime - dt.timedelta(days=lookback)
        # Construct a datetime of the day of the most recent record at midnight
        threshold_date = threshold.date()
        midnight = dt.datetime.min.time()
        threshold_dt = dt.datetime.combine(threshold_date, midnight)
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

    # Consolidate the records to only the highest value for each day
    df.index = pd.to_datetime(df["record_datetime"]).dt.date

    # Capitalize the period for labels
    label = period.capitalize()

    # Create columns for day of week number and name
    if period == "month":
        df[f"{label} Number"] = pd.to_datetime(df["record_datetime"]).dt.month
        df[f"{label} Name"] = (
            pd.to_datetime(df["record_datetime"]).dt.month_name()
        )
    else:
        df[f"{label} Number"] = pd.to_datetime(df["record_datetime"]).dt.dayofweek
        df[f"{label} Name"] = (
            pd.to_datetime(df["record_datetime"]).dt.day_name()
        )

    # Count the number of records for each day of the week
    group_columns = [f"{label} Number", f"{label} Name"]
    df = df.groupby(group_columns).size().reset_index(name="Count")

    # Ensure that the days are in the correct order
    df = df.sort_values(by=f"{label} Number", ascending=True)
    
    # Return the fully constructed dataframe
    return df