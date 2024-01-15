from flask import (
    Blueprint, flash, make_response, render_template, redirect, request,
    Response, session,
)

from ...extensions import db
from ...models import User, Password
from ...utilities import get_all_records_for_user


blueprint_account = Blueprint(
    "account",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/account/static",
)

@blueprint_account.route("/account")
def account() -> str | Response:
    """Page that allows the user to view and manage account information."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")

    # Get the user from the user id
    user = User.query.filter_by(user_id=user_id).one()

    # Get the datetime of the last time the user's password was changed
    password_id = user.password_id
    password_history = db.session.query(Password).filter_by(user_id=user_id)
    last_updated = password_history.order_by(Password.updated_datetime.desc())
    last_updated = last_updated.one().updated_datetime
    last_updated = last_updated.strftime(r"%B %-d, %Y %-I:%M:%S %p")

    # Otherwise, proceed to the user's account page
    return render_template(
        "/account/account.html",
        user=user,
        password_changed=last_updated,
    )

@blueprint_account.route("/account/export_data")
def export_data() -> Response:
    """Gets all of the user's records and downloads them as a csv file."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")
    
    # Pull all of the user's records
    user = User.query.filter_by(user_id=user_id).one()
    record_df = get_all_records_for_user(user)

    # Specify the filename for the csv file
    filename = f"manymiles_{user.username}.csv"

    # Drop any unnecessary columns
    record_df = record_df.drop(columns=[
        "record_id",
        "user_id",
        "create_datetime",
        "update_datetime",
    ])

    # Construct and return the response
    response = make_response(record_df.to_csv(index=False))
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response