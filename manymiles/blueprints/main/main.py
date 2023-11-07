import pandas as pd
from flask import Blueprint, render_template


blueprint_main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/index/static",
)


@blueprint_main.route("/")
@blueprint_main.route("/home")
def home() -> str:
    """"""
    return render_template("index/home.html")

@blueprint_main.route("/records")
def records() -> str:
    """"""
    return render_template("index/records.html")

@blueprint_main.route("/_get_records", methods=["GET", "POST"])
def _get_records() -> str:
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9],
    })
    return df.to_json(orient="split", index=False)