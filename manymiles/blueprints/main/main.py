import pandas as pd
from flask import Blueprint, render_template, redirect, session


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
    """"""
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("main/home.html")

@blueprint_main.route("/records")
def records() -> str:
    """"""
    return render_template("main/records.html")

@blueprint_main.route("/_get_records", methods=["GET", "POST"])
def _get_records() -> str:
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9],
    })
    return df.to_json(orient="split", index=False)