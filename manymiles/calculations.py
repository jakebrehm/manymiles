import datetime as dt

import pandas as pd

from .extensions import db
from .models import Record


# def get_average_mileage(df: pd.DataFrame) -> int:
#     """Calculates the average mileage from the first record to now."""

#     # Get the mileage and datetime of the earliest record
#     start_mileage = df["recorded_datetime"]
#     start_datetime = ...

#     # Get the mileage of the most recent record
#     end_mileage = ...

#     # Get the current datetime
#     end_datetime = ...