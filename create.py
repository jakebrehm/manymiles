#!/usr/bin/env python

"""
Creates the database for use in the application.
"""


from flask_sqlalchemy import SQLAlchemy

from app import load_config, create_app
from manymiles.extensions import db
from manymiles.models import Role


def create_database(database: SQLAlchemy) -> None:
    """Initializes the Flask application and uses it to initialize the database.
    
    Intended to be called from the command line to set up the project."""

    # Load the configuration
    load_config()
    
    # Create the application
    app = create_app()

    # Initialize the database
    with app.app_context():

        # Create the database
        database.create_all()

        # Fill out the role table
        database.session.add(Role(name="Owner"))
        database.session.add(Role(name="Admin"))
        database.session.add(Role(name="User"))
        database.session.add(Role(name="Read-Only"))
        database.session.commit()


if __name__ == '__main__':
    create_database(database=db)