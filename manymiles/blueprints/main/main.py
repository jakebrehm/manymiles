import pandas as pd
from flask import Blueprint, render_template, redirect, session

from ...extensions import db
from ...models import Record


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

@blueprint_main.route("/records", defaults={"page_num": 1, "per_page": 10})
@blueprint_main.route("/records/<int:page_num>", defaults={"per_page": 10})
@blueprint_main.route("/records/<int:page_num>/<int:per_page>")
def records(page_num: int, per_page: int) -> str:
    """"""

    # 
    if not (user_id := session["user_id"]):
        return redirect("/login")
    
    filtered_records = Record.query.filter_by(user_id=user_id)
    ordered_records = filtered_records.order_by(Record.mileage.desc())
    paginated_records = ordered_records.paginate(
        per_page=per_page,
        page=page_num,
        error_out=True,
    )

    return render_template(
        "main/records.html",
        records=paginated_records,
    )

@blueprint_main.route("/_get_records", methods=["GET", "POST"])
def _get_records() -> str:
    # df = pd.DataFrame({
    #     "A": [1, 2, 3],
    #     "B": [4, 5, 6],
    #     "C": [7, 8, 9],
    # })

    # user_id = session["user_id"]
    # if not user_id:
    if not (user_id := session["user_id"]):
        return redirect("/login")
    
    records = Record.query.filter_by(user_id=user_id).order_by(Record.mileage.desc()).paginate(per_page=10, page=1, error_out=True)
    # print(pd.DataFrame.from_records(item.__dict__ for item in records.items).columns)
    df = pd.DataFrame.from_records(item.__dict__ for item in records.items)
    # print(df.head())
    df["date"] = pd.to_datetime(df["recorded_datetime"]).dt.date.astype("string")
    df["time"] = pd.to_datetime(df["recorded_datetime"]).dt.time.astype("string")
    df = df[["record_id", "date", "time", "mileage", "notes"]]
    df = df.rename(columns={
        "record_id": "ID",
        "date": "Date",
        "time": "Time",
        "mileage": "Mileage",
        "notes": "Notes",
    })
    return df.to_json(orient="split", index=False)