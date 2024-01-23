import datetime as dt

from flask import (
    Blueprint, flash, render_template, redirect, request, Response, session
)

from ...extensions import db
from ...models import User
from ...utilities import (
    create_account, generate_hash, get_user_from_username, is_correct_password,
    is_username_available, is_valid_email, is_valid_password, is_valid_username,
    log_login,
)


blueprint_login = Blueprint(
    "login",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/login/static",
)

@blueprint_login.route("/register")
def register() -> str:
    """"""
    return render_template("login/register.html")

@blueprint_login.route("/login")
def login() -> str:
    """"""
    return render_template("login/login.html")

@blueprint_login.route("/logout")
def logout() -> Response:
    """Log the user out from their session."""

    # Clear the user's information from the session
    for key in list(session.keys()):
        session.pop(key)

    # Redirect the user to the homepage
    return redirect("/")

@blueprint_login.route("/validate_login", methods=["POST"])
def validate_login() -> Response:
    """Validate and perform the user's login request."""

    # Get the relevant information from the form
    username = request.form.get("username")
    password = request.form.get("password")
    remember = request.form.get("remember")

    # Get the user object
    user = get_user_from_username(username)

    # Check if any of the required values are blank
    if any(value is None for value in [username, password]):
        flash("Please provide values for all required inputs.")
        return redirect("/login")

    # Check that the user exists
    if not user:
        flash("An account with that username doesn't exist.")
        return redirect("/login")

    # Check if the username/password combination is correct
    if not is_correct_password(user, password):
        flash("The password entered does not match the one we have on file.")
        log_login(user, successful=False)
        return redirect("/login")
    
    # Add login to the history table
    log_login(user, successful=True)

    # Store the user's details in the session
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["first_name"] = user.first_name
    session["last_name"] = user.last_name
    session["email"] = user.email

    # Remember the user's details for a while if desired
    if remember == "on":
        session.permanent = True
    
    # Send the user to the homepage
    return redirect("/")

@blueprint_login.route("/add_user", methods=["POST"])
def add_user() -> Response:
    """Creates an account and adds the user to the database."""

    # Get the relevant information from the form
    username = request.form.get("username")
    email = request.form.get("email")
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")

    # Get a list of required keys
    optional_keys = ["first-name", "last-name"]
    required_keys = request.form.to_dict()
    for optional_key in optional_keys:
        required_keys.pop(optional_key, None)

    # Check if any of the required values are blank
    if any(value is None for value in required_keys.values()):
        flash("Please provide values for all required inputs.")
        return redirect("/register")

    # Confirm that the requested username is available
    if not is_username_available(username):
        flash("The requested username has already been taken.")
        return redirect("/register")

    # Confirm that the requested username is long enough
    if not is_valid_username(username):
        flash(
            "The username must be between 3 and 30 characters long, "
            "and the first character must not be a number."
        )
        return redirect("/register")

    # Confirm that the passwords are valid
    if not is_valid_password(password):
        # Don't need to check other password since it needs to be the same
        flash(
            "The password you entered is not valid. "
            "The password must be at least 7 characters long and include "
            "one lowercase letter, one uppercase letter, one number, and "
            "one special character."
        )
        return redirect("/register")

    # Confirm that the passwords match
    if not (password == confirm_password):
        flash("The provided passwords do not match.")
        return redirect("/register")
    
    # Confirm that the email is valid
    if not is_valid_email(email):
        flash("The email provided is not valid.")
        return redirect("/register")

    # Create the user's account with the requested details
    hash, salt = generate_hash(password)
    user = User(
        username=username,
        password_salt=salt,
        email=email,
        first_name=first_name,
        last_name=last_name,
        created=dt.datetime.now(),
    )
    create_account(user, hash)

    # Store the user's details in the session
    session["user_id"] = user.user_id
    session["username"] = user.username
    session["first_name"] = user.first_name
    session["last_name"] = user.last_name
    session["email"] = user.email

    # Redirect to the login screen on successful account creation
    return redirect("/")