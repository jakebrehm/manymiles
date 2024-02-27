#!/usr/bin/env python

"""
Deletes the application's database.
"""


from flask_sqlalchemy import SQLAlchemy

from app import load_config, create_app
from manymiles.extensions import db


def delete_database(database: SQLAlchemy) -> None:
    """Initializes the Flask application and uses it to delete the database.
    
    Intended to be called from the command line to tear down the project."""

    # Load the configuration
    load_config()
    
    # Create the application
    app = create_app()

    # Initialize the database
    with app.app_context():
        database.drop_all()


if __name__ == '__main__':
    delete_database(database=db)