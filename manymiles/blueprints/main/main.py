"""
Contains routes for the main portion of the application, i.e., the homepage and
related/required pages.
"""


import datetime as dt

import pandas as pd
from flask import (
    Blueprint, jsonify, render_template, redirect, session, request, Response
)

from ... import calculations
from ...utilities import (
    get_all_records_for_user, get_current_user_id, get_user_from_id,
    login_required
)


blueprint_main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/main/static",
)


@blueprint_main.route("/")
@blueprint_main.route("/home")
@login_required()
def home() -> str | Response:
    """The home page of the application."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
    try:
        # Determine the unique days that the user has make records on
        columns = ["record_datetime", "mileage"]
        df = get_all_records_for_user(user_id)[columns]
        n_records = len(df)
        df.index = pd.to_datetime(df["record_datetime"]).dt.date
        df = df.groupby(df.index).max()
        n_days = len(df)
        show_visualizations = (n_records >= 2) and (n_days >= 2)
    except KeyError:
        show_visualizations = False

    # Otherwise, proceed to the homepage
    return render_template(
        "main/home.html",
        user=get_user_from_id(user_id),
        show_visualizations=show_visualizations,
    )


@blueprint_main.route("/data/record-timeline", methods=["GET"])
@login_required()
def get_record_timeline() -> Response:
    """Gets the data necessary to create the record timeline visualization."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()

    # Get the value of query parameters from the request
    period = request.args.get("period")

    # Determine how much data to pull according to the query parameters
    lookback = {
        "week": 7,
        "month": 30,
        "year": 365,
    }.get(period, None)

    # Attempt to grab the data used for making the record timeline visualization
    try:
        df = calculations.create_record_timeline_df(user_id, lookback)
    except KeyError:
        return jsonify({"valid": False})

    # Separate the records in the record dates and mileage values
    labels = [date.strftime(r"%m-%d-%Y") for date in df.index.tolist()]
    values = df["mileage"].tolist()

    # Return the data as a json
    return jsonify({"valid": True, "labels": labels, "values": values})


@blueprint_main.route("/data/record-frequency", methods=["GET"])
@login_required()
def get_record_frequency() -> Response:
    """Gets the data necessary to create the record frequency visualization."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()

    # Get the value of query parameters from the request
    period = request.args.get("period", default="day")

    # Attempt to grab the data used for making the record timeline visualization
    try:
        df = calculations.create_record_frequency_df(user_id, period=period)
    except KeyError:
        return jsonify({"valid": False})

    # Separate the records in the record dates and mileage values
    labels = df[f"{period.capitalize()} Name"].tolist()
    values = df["Count"].tolist()

    # Return the data as a json
    return jsonify({"valid": True, "labels": labels, "values": values})