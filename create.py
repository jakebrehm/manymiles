#!/usr/bin/env python

"""
Creates the database for use in the application.
"""


from flask_sqlalchemy import SQLAlchemy

from app import load_config, create_app
from manymiles.extensions import db


def initialize_database(database: SQLAlchemy) -> None:
    """Initializes the Flask application and uses it to initialize the database.
    
    Intended to be called from the command line to set up the project."""

    # Load the configuration
    load_config()
    
    # Create the application
    app = create_app()

    # Initialize the database
    with app.app_context():
        database.create_all()


if __name__ == '__main__':
    initialize_database(database=db)