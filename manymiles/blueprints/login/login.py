from flask import Blueprint, render_template


bp_login = Blueprint(
    "login",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/login/static",
)


@bp_login.route("/register")
def register() -> str:
    """"""
    return render_template("login/register.html")

@bp_login.route("/login")
def login() -> str:
    """"""
    return render_template("login/login.html")