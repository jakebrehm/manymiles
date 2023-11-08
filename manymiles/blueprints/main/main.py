import datetime as dt
import math

from flask import (
    Blueprint, flash, render_template, redirect, request, session, url_for
)

from ...extensions import db
from ...models import Record
from ...utilities import get_datetime_from_string, get_string_from_datetime


blueprint_main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/main/static",
)

@blueprint_main.route("/")
@blueprint_main.route("/home")
def home() -> str:
    """The home page of the application."""
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("main/home.html")

@blueprint_main.route("/records", defaults={"page_num": 1, "per_page": 10})
@blueprint_main.route("/records/<int:page_num>", defaults={"per_page": 10})
@blueprint_main.route("/records/<int:page_num>/<int:per_page>")
def records(page_num: int, per_page: int) -> str:
    """Page that shows all records and allows the user to add new ones."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")

    # Get any optional filters
    from_timestamp = request.args.get("from")
    if from_timestamp:
        from_timestamp = get_datetime_from_string(from_timestamp)
    to_timestamp = request.args.get("to")
    if to_timestamp:
        to_timestamp = get_datetime_from_string(to_timestamp)
    
    # Check if the "from" timestamp is before the "to" timestamp
    if to_timestamp and from_timestamp and (from_timestamp > to_timestamp):
        flash(
            "The value of `Records from` must be before the value "
            "of `Records until`."
        )
        return redirect("/records")
    
    # Filter out records not created by the user
    filtered_records = Record.query.filter_by(user_id=user_id)
    # Filter out records outside of the specified timeframe
    if from_timestamp:
        filtered_records = filtered_records.filter(
            Record.recorded_datetime >= from_timestamp
        )
    if to_timestamp:
        filtered_records = filtered_records.filter(
            Record.recorded_datetime <= to_timestamp
        )

    # Order the records by descending mileage
    ordered_records = filtered_records.order_by(Record.mileage.desc())
    
    # Determine the number of pages that should be paginated
    n_records = len(ordered_records.all())
    n_pages = math.ceil(n_records / per_page)
    page_num = n_pages if (page_num > n_pages) else page_num

    # Paginate the filtered and ordered records
    paginated_records = ordered_records.paginate(
        per_page=per_page,
        page=page_num,
        error_out=True,
    )

    # Render the records page with the pagination
    return render_template(
        "main/records.html",
        records=paginated_records,
        to_timestamp=get_string_from_datetime(to_timestamp),
        from_timestamp=get_string_from_datetime(from_timestamp),
    )

@blueprint_main.route("/record/filter", methods=["GET", "POST"])
def filter_records() -> str:
    """Filters the records displayed on the application."""

    print(request.form.to_dict())
    parameters = request.form.to_dict()
    if "page_num" in parameters:
        parameters["page_num"] = 1
    print(request.form.to_dict())

    return redirect(url_for("main.records", **parameters))

@blueprint_main.route("/record/add", methods=["GET", "POST"])
def add_record() -> str:
    """Adds a record to the database."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")
    
    # Get the relevant information from the form
    timestamp = request.form.get("timestamp")
    mileage = int(request.form.get("mileage"))
    notes = request.form.get("notes")

    # Check if any of the required values are blank
    if any(value is None for value in [timestamp, mileage]):
        flash("Please provide values for all required inputs.")
        return redirect("/records")

    # Check if the mileage is below 0
    if mileage < 0:
        flash("Please enter a mileage that is greater than or equal to zero.")
        redirect("/records")

    # # Determine the highest mileage recorded by the user
    # filtered_records = db.session.query(Record).filter_by(user_id=user_id)
    # ordered_records = filtered_records.order_by(Record.mileage.desc())
    # highest_record = ordered_records.limit(1).first()

    # Add the record to the database
    db.session.add(Record(
        user_id=user_id,
        mileage=mileage,
        recorded_datetime=timestamp,
        notes=notes,
    ))
    db.session.commit()

    # Redirect back to the records page
    return redirect("/records")

@blueprint_main.route("/record/delete/<int:record_id>", methods=["GET", "POST"])
def delete_record(record_id: int):
    """Deletes a record from the database."""

    # Confirm that the user is logged in
    if not session.get("user_id", None):
        return redirect("/login")

    # Delete the record from the database
    record = Record.query.filter_by(record_id=record_id).one()
    db.session.delete(record)
    db.session.commit()

    # Redirect back to the records page with all parameters intact
    return redirect(url_for("main.records", **request.args.to_dict()))