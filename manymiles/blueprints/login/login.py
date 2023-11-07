from flask import (
    Blueprint, flash, render_template, redirect, request, Response, session
)

from ...extensions import db
from ...models import User
from ... import utilities


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
def logout() -> str:
    """Log the user out from their session."""

    # Clear the user's information from the session
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("first_name", None)
    session.pop("last_name", None)
    session.pop("email", None)

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
    user = db.session.query(User).filter_by(username=username).first()

    # If the user was not found, flash an alert
    if user is None:
        flash("An account with that username doesn't exist.")
        return redirect("/login")

    # If the username/password combination is incorrect, flash an alert
    if not utilities.is_correct_password(user, password):
        flash("The password entered does not match the one we have on file.")
        return redirect("/login")

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