from flask import Blueprint, render_template


bp_login = Blueprint("login", __name__, template_folder="templates")


@bp_login.route("/login")
def login() -> ...:
    """"""
    return render_template("login/login.html")

@bp_login.route("/register")
def register() -> ...:
    """"""
    return render_template("login/register.html")