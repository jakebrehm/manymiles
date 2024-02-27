"""
Provides an entry point to the database handle without causing circular imports.
"""


from flask_sqlalchemy import SQLAlchemy


# Initialize the database
db = SQLAlchemy()