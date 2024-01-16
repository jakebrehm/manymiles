from flask import (
    Blueprint, flash, make_response, render_template, redirect, request,
    Response, session, url_for
)

from ...extensions import db
from ...models import User, Password
from ...utilities import (
    generate_hash, get_all_records_for_user, get_user_from_id, is_valid_email,
    is_valid_password, update_current_password,
)


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
    last_updated = last_updated.first().updated_datetime
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

@blueprint_account.route("/account/update_email", methods=["POST"])
def update_email() -> Response:
    """Updates a user's email in the database."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")
    
    # Get the relevant information from the form
    new_email = request.form.get("new-email")

    # Confirm that the email is valid
    if not is_valid_email(new_email):
        flash("The email provided is not valid.")
        return redirect("/account")
    
    # Get the user with the associated user id
    user = get_user_from_id(user_id)

    # Change the user's email and commit the changes
    user.email = new_email
    db.session.commit()

    # Redirect back to the account page
    return redirect(url_for("account.account"))

@blueprint_account.route("/account/update_password", methods=["POST"])
def update_password() -> Response:
    """Updates a user's password in the database."""

    # Confirm that the user is logged in
    if not (user_id := session.get("user_id", None)):
        return redirect("/login")
    
    # Get the relevant information from the form
    old_password = request.form.get("old-password")
    new_password = request.form.get("new-password")
    confirm_password = request.form.get("confirm-password")

    # Get the user with the associated user id
    user = get_user_from_id(user_id=user_id)

    # Check that the old password is correct
    if not is_valid_password(old_password):
        # Don't need to check other password since it needs to be the same
        flash(
            "The password you entered is not valid. "
            "The password must be at least 7 characters long and include "
            "one lowercase letter, one uppercase letter, one number, and "
            "one special character."
        )
        return redirect("/account")

    # Check that the new password fields match
    if not (new_password == confirm_password):
        flash("The provided passwords do not match.")
        return redirect("/account")
    
    # Change the user's current password to the requested one
    hash, _ = generate_hash(new_password, salt=user.password_salt)
    update_current_password(user, hash)

    # Redirect back to the account page
    return redirect(url_for("account.account"))