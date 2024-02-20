from flask import (
    Blueprint, jsonify, render_template, redirect, session, Response
)

import pandas as pd

from ... import utilities
from ... import calculations


blueprint_main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/main/static",
)


@blueprint_main.route("/")
@blueprint_main.route("/home")
def home() -> str | Response:
    """The home page of the application."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")
    
    try:
        # Determine the unique days that the user has make records on
        columns = ["record_datetime", "mileage"]
        df = utilities.get_all_records_for_user(user_id)[columns]
        df.index = pd.to_datetime(df["record_datetime"]).dt.date
        df = df.groupby(df.index).max()
        show_visualizations = (len(df) >= 3)
    except KeyError:
        show_visualizations = False

    # Otherwise, proceed to the homepage
    return render_template(
        "main/home.html",
        user=utilities.get_user_from_id(user_id),
        show_visualizations=show_visualizations,
    )


@blueprint_main.route("/data/record-timeline", methods=["GET"])
def get_record_timeline() -> Response:
    """Gets the data necessary to create the record timeline visualization."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")

    try:
        # Grab the data used for making the record timeline visualization
        df = calculations.create_record_timeline_dataframe(user_id)
    except KeyError:
        return jsonify({"valid": False})

    # Separate the records in the record dates and mileage values
    labels = [date.strftime(r"%m-%d-%Y") for date in df.index.tolist()]
    values = df["mileage"].tolist()

    # Return the data as a json
    return jsonify({"valid": True, "labels": labels, "values": values})


@blueprint_main.route("/data/day-of-week-histogram", methods=["GET"])
def get_day_of_week_histogram() -> Response:
    """Gets the data necessary to create the day of week histogram."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")

    try:
        # Grab the data used for making the record timeline visualization
        df = calculations.create_day_of_week_histogram_dataframe(user_id)
    except KeyError:
        return jsonify({"valid": False})

    # Separate the records in the record dates and mileage values
    labels = df["Day Name"].tolist()
    values = df["Count"].tolist()

    # Return the data as a json
    return jsonify({"valid": True, "labels": labels, "values": values})