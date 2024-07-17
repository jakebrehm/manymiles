"""
Contains all application routes related to the account settings page, where the
user can change their username, password, delete their account, etc.
"""


import datetime as dt
from io import StringIO

import pandas as pd
import sqlalchemy as sa
from flask import (
    Blueprint, flash, make_response, render_template, redirect, request,
    Response, session, url_for
)

from ...extensions import db
from ...models import Record, User
from ...utilities import (
    delete_account, generate_hash, get_all_records_for_user, get_current_user_id,
    get_user_from_id, get_password_from_id, is_username_available, 
    is_valid_email, is_valid_name, is_valid_password, is_valid_username,
    login_required, update_current_password,
)


blueprint_account = Blueprint(
    "account",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/account/static",
)


@blueprint_account.route("/account")
@login_required()
def account() -> str | Response:
    """Page that allows the user to view and manage account information."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()

    # Get the user from the user id
    user = User.query.filter_by(user_id=user_id).one()

    # Get the datetime of the last time the user's password was changed
    password = get_password_from_id(password_id=user.password_id)
    last_updated = password.updated_datetime

    # Otherwise, proceed to the user's account page
    return render_template(
        "/account/account.html",
        user=user,
        password_changed=last_updated.strftime(r"%B %-d, %Y %-I:%M:%S %p"),
    )


@blueprint_account.route("/account/import_data", methods=["POST"])
@login_required()
def import_data() -> Response:
    """Imports data from a csv file and replaces the user's records."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()

    # Check if the records was posted by the form
    if request.method == "POST":
        # Get the file from the request
        file = request.files["recordsToImport"]
        try:
            # Read the file into a dataframe
            df = pd.read_csv(StringIO(file.read().decode("utf-8")))
            # Remove all of the user's records
            db.session.query(Record).filter_by(user_id=user_id).delete()
            # Add the new records
            for row in df.iterrows():
                notes = row[1]["notes"]
                db.session.add(Record(
                    user_id=user_id,
                    mileage=row[1]["mileage"],
                    record_datetime=row[1]["record_datetime"],
                    create_datetime=dt.datetime.now(),
                    update_datetime=dt.datetime.now(),
                    notes=None if pd.isnull(notes) else notes,
                ))
            # Commit the changes
            db.session.commit()
        except Exception as e:
            print(e)
            # If there was an error, flash a message
            flash(
                "There was an error importing your data. "
                "Please make sure that the file is in the correct format."
            )
    
    # Redirect back to the account page
    return redirect(url_for("account.account"))


@blueprint_account.route("/account/export_data")
@login_required()
def export_data() -> Response:
    """Gets all of the user's records and downloads them as a csv file."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
    # Pull all of the user's records
    user = User.query.filter_by(user_id=user_id).one()
    try:
        record_df = get_all_records_for_user(user)
    except KeyError:
        # If there was a KeyError, that means there is no data to export
        flash("You have no records to export.")
        return redirect("/account")

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


@blueprint_account.route("/account/update_username", methods=["POST"])
@login_required()
def update_username() -> Response:
    """Updates a user's username in the database."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
    # Get the relevant information from the form
    new_username = request.form.get("new-username")

    # Get the user with the associated user id
    user = get_user_from_id(user_id)

    # Confirm that the requested username does not match the current one
    if new_username == user.username:
        flash(
            "The username you requested is the same as your current username."
        )
        return redirect("/account")

    # Confirm that the username is valid
    if not is_valid_username(new_username):
        flash(
            "The new username must be between 3 and 30 characters long, "
            "and the first character must not be a number."
        )
        return redirect("/account")

    # Confirm that the username is valid
    if not is_username_available(new_username):
        flash("The requested username has already been taken.")
        return redirect("/account")

    # Change the user's email and commit the changes
    user.username = new_username
    db.session.commit()

    # Change the user's username in the session
    session["username"] = new_username

    # Redirect back to the account page
    return redirect(url_for("account.account"))


@blueprint_account.route("/account/update_name", methods=["POST"])
@login_required()
def update_name() -> Response:
    """Updates a user's first and last name in the database."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
    # Get the relevant information from the form
    new_first_name = request.form.get("new-first-name")
    new_last_name = request.form.get("new-last-name")

    # Confirm that the names are valid
    if not is_valid_name(new_first_name):
        flash("The first name provided is not valid.")
        return redirect("/account")
    elif not is_valid_name(new_last_name):
        flash("The last name provided is not valid.")
        return redirect("/account")
    
    # Get the user with the associated user id
    user = get_user_from_id(user_id)

    # Change the user's first and last names and commit the changes
    user.first_name = new_first_name if new_first_name else sa.null()
    user.last_name = new_last_name if new_last_name else sa.null()
    db.session.commit()

    # Change the user's name in the session
    session["first_name"] = new_first_name
    session["last_name"] = new_last_name

    # Redirect back to the account page
    return redirect(url_for("account.account"))


@blueprint_account.route("/account/update_email", methods=["POST"])
@login_required()
def update_email() -> Response:
    """Updates a user's email in the database."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
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

    # Change the user's email in the session
    session["email"] = new_email

    # Redirect back to the account page
    return redirect(url_for("account.account"))


@blueprint_account.route("/account/update_password", methods=["POST"])
@login_required()
def update_password() -> Response:
    """Updates a user's password in the database."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
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


@blueprint_account.route("/account/delete_account")
@login_required()
def delete_user_account() -> Response:
    """Delete's all traces of a user's account from the database."""

    # Get the currently signed in user's id
    user_id = get_current_user_id()
    
    # Get the user and delete their account
    user = get_user_from_id(user_id=user_id)
    delete_account(user)

    # Clear the user's information from the session
    for key in list(session.keys()):
        session.pop(key)

    # Flash a goodbye message
    flash("Your account has been deleted. Thanks for using ManyMiles!")

    # Redirect back to the account page
    return redirect(url_for("login.register"))