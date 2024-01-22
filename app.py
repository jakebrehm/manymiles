import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask

from manymiles.blueprints.account.account import blueprint_account
from manymiles.blueprints.api.api import blueprint_api, create_api
from manymiles.blueprints.errors.errors import blueprint_errors
from manymiles.blueprints.main.main import blueprint_main
from manymiles.blueprints.login.login import blueprint_login
from manymiles.blueprints.records.records import blueprint_records
from manymiles.extensions import db
from manymiles.utilities import get_env_bool


def load_config(env_path: Optional[str]=None) -> None:
    """Loads environmental variables from the .env file."""

    # Specify the path to the env file
    if env_path is None:
        env_path = r"cfg/.env"
    
    # Only attempt to load the environment variables if the file exists
    if os.path.isfile(env_path):
        load_dotenv(env_path, override=True)


def create_app() -> Flask:
    """Creates and return the Flask application."""

    # Create the application
    root_path = os.path.join(os.getcwd(), "manymiles")
    app = Flask(__name__, root_path=root_path)
    # Set the secret key
    app.secret_key = os.environ.get("MM_FLASK_SECRET")
    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("MM_DATABASE_URI")

    # Initialize the database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(blueprint_account)
    app.register_blueprint(blueprint_api)
    app.register_blueprint(blueprint_errors)
    app.register_blueprint(blueprint_main)
    app.register_blueprint(blueprint_login)
    app.register_blueprint(blueprint_records)

    # Return the application
    return app


if __name__ == "__main__":
    load_config()
    app = create_app()
    create_api(app)
    app.run(
        host=os.getenv("MM_FLASK_HOST"),
        port=os.getenv("PORT"),
        debug=get_env_bool("MM_FLASK_DEBUG"),
    )