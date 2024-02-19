import datetime as dt

import pandas as pd

from . import utilities
from .extensions import db
from .models import Record, User


# def get_average_mileage(df: pd.DataFrame) -> int:
#     """Calculates the average mileage from the first record to now."""

#     # Get the mileage and datetime of the earliest record
#     start_mileage = df["recorded_datetime"]
#     start_datetime = ...

#     # Get the mileage of the most recent record
#     end_mileage = ...

#     # Get the current datetime
#     end_datetime = ...


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