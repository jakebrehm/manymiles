#!/usr/bin/env python

"""
Updates the database for use in the application.
"""


from flask_sqlalchemy import SQLAlchemy

from app import load_config, create_app
from manymiles.extensions import db


def create_database(database: SQLAlchemy) -> None:
    """Updates the database with any new models.
    
    Intended to be called from the command line to set up the project."""

    # Load the configuration
    load_config()
    
    # Create the application
    app = create_app()

    # Initialize the database
    with app.app_context():

        # Create the database
        database.create_all()


if __name__ == '__main__':
    create_database(database=db)