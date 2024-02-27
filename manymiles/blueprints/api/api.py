"""
Contains code related to the creation of the RESTful API.
"""


from flask import Blueprint, Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from .user import UserAPI
from .authenticate import AuthenticateAPI
from .records import MostRecentRecordAPI, RecordAPI


blueprint_api = Blueprint(
    "api",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/api/static",
)


blueprint_api_docs = get_swaggerui_blueprint(
    base_url="/api/docs",
    api_url="/api/static/swagger.json",
)


def create_api(app: Flask) -> None:
    """Creates the API instance so that it can be used from the main script.
    
    Encapsulating the contents of this function was required in order to avoid
    circular references/imports and trying to use an unavailable application
    context.
    """

    # Create the API instance
    api = Api(app)

    # Add the API resources
    api.add_resource(
        UserAPI,
        "/api/user",
    )
    api.add_resource(
        AuthenticateAPI,
        "/api/authenticate"
    )
    api.add_resource(
        RecordAPI,
        "/api/record",
    )
    api.add_resource(
        MostRecentRecordAPI,
        "/api/record/most-recent",
    )