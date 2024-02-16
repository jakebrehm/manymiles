from flask import (
    Blueprint, render_template, redirect, session, Response
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
def home() -> str | Response:
    """The home page of the application."""

    # Confirm that the user is logged in
    if not session.get("user_id", None):
        return redirect("/login")
    
    # Otherwise, proceed to the homepage
    return render_template("main/home.html")