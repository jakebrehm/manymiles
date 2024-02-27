"""
Contains routes for portions of the application related to error handling, such
as a route that is specifically for informing the user that the requested route
does not exist (404).
"""


from typing import Type

from flask import (
    Blueprint, render_template
)


blueprint_errors = Blueprint(
    "errors",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/errors/static",
)


@blueprint_errors.app_errorhandler(404)
def page_not_found(error: Type[Exception]) -> str:
    """Navigates to a custom 404 error page if a page was not found."""

    # Proceed to the "page not found" page
    return render_template("errors/404.html"), 404