from flask import (
    Blueprint, jsonify, render_template, redirect, session, Response
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
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("main/home.html")

@blueprint_main.route("/get_daily_data")
def get_daily_data() -> Response:
    """"""

    return jsonify({
        "data": [1, 2, 4, 6, 7, 8, 10],
    })