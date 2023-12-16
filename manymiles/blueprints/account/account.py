from flask import (
    Blueprint, flash, render_template, redirect, request, Response, session
)

from ...extensions import db
from ...models import User


blueprint_account = Blueprint(
    "account",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/account/static",
)

@blueprint_account.route("/account")
def account() -> str | Response:
    """Page that allows the user to view and manage account information."""
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("/account/account.html")