from flask import (
    Blueprint, render_template, redirect, request, Response, session
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

@blueprint_login.route("/validate_login", methods=["POST"])
def validate_login() -> Response:
    """"""
    username = request.form.get("username")
    password = request.form.get("password")
    remember = request.form.get("remember")

    print(f"{username=}")
    print(f"{password=}")
    print(f"{remember=}")

    # session["user_id"] = 
    session["username"] = username

    if remember == "on":
        session.permanent = True
    

    return redirect("/")