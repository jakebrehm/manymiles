import datetime as dt

from flask import Blueprint, flash, render_template, redirect, request, session

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
    
    # Paginate the records to display in a table
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
    ordered_records = filtered_records.order_by(Record.mileage.desc())
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

    # Determine the highest mileage recorded by the user
    filtered_records = db.session.query(Record).filter_by(user_id=user_id)
    ordered_records = filtered_records.order_by(Record.mileage.desc())
    highest_record = ordered_records.limit(1).first()

    # Check if the entered mileage is higher than the previous mileages
    if highest_record and not (mileage >= highest_record.mileage):
        flash("You cannot record a lower mileage than your previous records.")
        return redirect("/records")

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