import os

from dotenv import load_dotenv
from flask import Flask

from manymiles.blueprints.account.account import blueprint_account
from manymiles.blueprints.api.api import blueprint_api, create_api
from manymiles.blueprints.main.main import blueprint_main
from manymiles.blueprints.login.login import blueprint_login
from manymiles.blueprints.records.records import blueprint_records
from manymiles.extensions import db


def create_app() -> Flask:
    """Creates and return the Flask application."""

    # Load the configuration variables
    load_dotenv(r"cfg/.env", override=True)

    # Create the application
    root_path = os.path.join(os.getcwd(), "manymiles")
    app = Flask(__name__, root_path=root_path)
    # Set the secret key
    app.secret_key = os.environ.get("MM_SECRET_KEY")
    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("MM_URI")

    # Initialize the database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(blueprint_account)
    app.register_blueprint(blueprint_api)
    app.register_blueprint(blueprint_main)
    app.register_blueprint(blueprint_login)
    app.register_blueprint(blueprint_records)

    # Return the application
    return app


if __name__ == "__main__":
    app = create_app()
    create_api(app)
    app.run(debug=True)