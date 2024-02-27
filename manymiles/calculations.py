"""
Performs calculations and operations related to metrics and visualizations.
"""


import pandas as pd

from . import utilities
from .models import User


def create_record_timeline_dataframe(user: User | int) -> pd.DataFrame:
    """Creates the dataframe that is used for the record timeline chart."""

    # Get all records for the specified user
    columns = ["record_datetime", "mileage"]
    df = utilities.get_all_records_for_user(user)[columns]

    # Get the maximum mileage value for each day
    df.index = df["record_datetime"]
    df = df.groupby(pd.Grouper(freq="D")).max()

    # Back fill any missing dates
    df["mileage"] = df["mileage"].ffill()

    # Drop the extra datetime column
    df = df.drop(labels=["record_datetime"], axis=1)

    # Return the fully constructed dataframe
    return df


def create_day_of_week_histogram_dataframe(user: User | int) -> pd.DataFrame:
    """Creates the dataframe that is used for the day of week histogram."""

    # Get all records for the specified user
    columns = ["record_datetime", "mileage"]
    df = utilities.get_all_records_for_user(user)[columns]

    # Consolidate the records to only the highest value for each day
    df.index = pd.to_datetime(df["record_datetime"]).dt.date
    df = df.groupby(df.index).max()

    # Create columns for day of week number and name
    df["Day Number"] = pd.to_datetime(df["record_datetime"]).dt.dayofweek
    df["Day Name"] = pd.to_datetime(df["record_datetime"]).dt.day_name()

    # Count the number of records for each day of the week
    group_columns = ["Day Number", "Day Name"]
    df = df.groupby(group_columns).size().reset_index(name="Count")

    # Ensure that the days are in the correct order
    df = df.sort_values(by="Day Number", ascending=True)
    
    # Return the fully constructed dataframe
    return df


def create_month_histogram_dataframe(user: User | int) -> pd.DataFrame:
    """Creates the dataframe that is used for the month histogram."""

    # Get all records for the specified user
    columns = ["record_datetime", "mileage"]
    df = utilities.get_all_records_for_user(user)[columns]

    # Consolidate the records to only the highest value for each month
    df.index = pd.to_datetime(df["record_datetime"]).dt.date
    df = df.groupby(df.index).max()

    # Create columns for month number and name
    df["Month Number"] = pd.to_datetime(df["record_datetime"]).dt.month
    df["Month Name"] = pd.to_datetime(df["record_datetime"]).dt.month_name()

    # Count the number of records for each month
    group_columns = ["Month Number", "Month Name"]
    df = df.groupby(group_columns).size().reset_index(name="Count")

    # Ensure that the months are in the correct order
    df = df.sort_values(by="Month Number", ascending=True)
    
    # Return the fully constructed dataframe
    return df
