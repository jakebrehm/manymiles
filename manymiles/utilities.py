"""
Contains miscellaneous utility and helper functions for use in the project.
"""


import datetime as dt
import hashlib
import os
import re
from distutils.util import strtobool
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
import sqlalchemy as sa
from flask import redirect, Request, Response, session

from .extensions import db
from . import models


def get_env_bool(name: str) -> bool:
    """Reads an environmental variable as a boolean value."""
    return bool(strtobool(os.getenv(name, default="False")))


def generate_hash(
    password: str,
    salt: Optional[bytes] = None,
) -> tuple[str, str]:
    """Hashes the provided password and generates a salt for the user.
     
    Uses the MD5 algorithm. A salt can be provided as an argument if the user
    already exists (e.g., is just changing their password) instead of generating
    a new one each time.
    """

    # Generate a random salt for the user if one is not provided
    if salt is None:
        salt = os.urandom(10)

    # Generate the hash for the password
    h = hashlib.new("SHA256")
    h.update(salt + password.encode())

    # Return the hash and salt
    return h.hexdigest(), salt


def is_correct_password(user: models.User, password_to_verify: str) -> bool:
    """Returns whether or not the provided password is correct for the user."""

    # Get the user's current password information
    password = get_password_from_id(password_id=user.password_id)

    # Hash and salt the provided password
    h = hashlib.new("SHA256")
    h.update(user.password_salt + password_to_verify.encode())

    # Compare the two hashes and return the result
    return (password.password_hash == h.hexdigest())


def get_user_from_id(user_id: int) -> models.User | None:
    """Gets a user from a user id."""

    # Return the password row that matches the provided id
    return models.User.query.filter_by(user_id=user_id).first()


def get_user_from_username(username: int) -> models.User | None:
    """Gets a user from a username."""

    # Return the password row that matches the provided username
    return models.User.query.filter_by(username=username).first()


def get_password_from_id(password_id: int) -> models.Password | None:
    """Gets a user's password from a password id."""

    # Return the password row that matches the provided id
    return models.Password.query.filter_by(password_id=password_id).first()


def get_role_by_id(role_id: int) -> models.Role | None:
    """Gets a role by an id number."""

    # Return the role row that matches the provided id
    return models.Role.query.filter_by(role_id=role_id).first()


def get_role_by_name(role_name: str) -> models.Role | None:
    """Gets a role by role name."""

    # Return the role row that matches the provided id
    return models.Role.query.filter_by(name=role_name).first()


def add_user_role(user: models.User, role: models.Role) -> None:
    """Assigns the requested role for the provided user."""

    # Add the role to the user role table
    user_role = models.UserRole(
        user_id=user.user_id,
        role_id=role.role_id,
    )
    db.session.add(user_role)
    db.session.commit()


def update_current_password(user: models.User, password_hash: str) -> None:
    """Adds the user's current password to the password history table.
    
    Also updates the `password_id` column of the User record.

    Should be called after the user's password is updated and committed.
    """

    # Add their password to the password table
    password = models.Password(
        user_id=user.user_id,
        password_hash=password_hash,
        updated_datetime=dt.datetime.now(),
    )
    db.session.add(password)
    db.session.commit()

    # Link password back to the user
    user.password_id = password.password_id
    db.session.commit()


def log_login(user: models.User, successful: bool) -> None:
    """Records the user's successful login in the login history table."""

    # Add the login to the database
    row = models.Login(
        user_id=user.user_id,
        login_datetime=dt.datetime.now(),
        successful=successful,
    )
    db.session.add(row)
    db.session.commit()


def log_api_request(user: models.User, request: Request, status: int) -> None:
    """Records an API request in the API Request table."""

    # Add the API request to the database
    row = models.ApiRequest(
        user_id=user.user_id,
        endpoint=request.path,
        method=request.method,
        status=status,
        request_datetime=dt.datetime.now(),
    )
    db.session.add(row)
    db.session.commit()


def create_account(
    user: models.User,
    password_hash: str,
    role_id: Optional[int] = 3,
) -> None:
    """Creates an account and adds it to the database.
    
    Also adds a record to the password history table.
    """

    # Create a user object and add it to the database
    db.session.add(user)
    db.session.commit()

    # Log the user's password in the password table
    update_current_password(user, password_hash)

    # Log the user's successful login to the database
    log_login(user, successful=True)

    # Give the user the specified role
    role = get_role_by_id(role_id)
    add_user_role(user, role)


def delete_account(
    user: models.User,
) -> None:
    """Deletes all traces of a user's account from the database."""
    
    # Get the user's id
    user_id = user.user_id

    # Set the user's password id to null to avoid integrity errors
    user.password_id = sa.null()
    db.session.commit()

    # Delete all of the user's data in the login table
    logins = models.Login.query.filter_by(user_id=user_id).all()
    for login in logins:
        db.session.delete(login)

    # Delete the user's data in the user-role table
    user_roles = models.UserRole.query.filter_by(user_id=user_id).all()
    for user_role in user_roles:
        db.session.delete(user_role)

    # Delete all of the user's data in the record table
    records = models.Record.query.filter_by(user_id=user_id).all()
    for record in records:
        db.session.delete(record)

    # Delete all of the user's data in the password table
    passwords = models.Password.query.filter_by(user_id=user_id).all()
    for password in passwords:
        db.session.delete(password)

    # Delete the user's data in the user table
    db.session.delete(user)

    # Commit the previous transactions
    db.session.commit()


def is_username_available(username: str) -> bool:
    """Checks whether or not the provided username is available."""
    
    # See if there are any matches for the username in the database
    matched = db.session.query(models.User).filter_by(username=username).first()
    # Return if the username is available
    return (username != matched.username) if matched else True


def is_valid_username(username: str) -> bool:
    """Checks whether or not the provided username is valid."""
    valid_length = (3 <= len(username) <= 30)
    first_character = (not username[0].isnumeric())
    no_special_characters = username.isalnum()
    return valid_length and first_character and no_special_characters


def is_valid_name(name: str) -> bool:
    """Checks whether or not the provided name is valid."""
    return (name.isalpha() and (len(name) <= 64)) or not name


def is_valid_email(email: str) -> bool:
    """Checks whether or not the provided email is valid."""
    expression = r"^[a-z0-9]+([\._]?[a-z0-9]+)*[@]\w+[.]\w{2,3}$"
    return bool(re.match(expression, email))


def is_valid_password(password: str) -> bool:
    """Checks whether or not the provided password is valid.
    
    The password must be at least 7 characters long and include one lowercase
    letter, one uppercase letter, one number, and one special character.
    """
    
    expression = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{7,}$"
    return bool(re.match(expression, password))


def get_datetime_from_string(
    string: Optional[str],
    format: Optional[str] = None,
) -> dt.datetime:
    """Converts a datetime string of the given format to a datetime object."""

    # Set a default format if one is not provided
    if format is None:
        format = r"%Y-%m-%dT%H:%M"
    
    # If the string input is not valid, pass it through
    if not string:
        return string
    
    # Trim the datetime string if necessary
    if len(string) >= 16:
        string = string[:16]

    # Otherwise, convert to a datetime object and return
    return dt.datetime.strptime(string, format)


def get_string_from_datetime(
    timestamp: Optional[dt.datetime],
    format: Optional[str] = None,
) -> dt.datetime:
    """Converts a datetime object to a datetime string with a given format."""

    # Set a default format if one is not provided
    if format is None:
        format = r"%Y-%m-%dT%H:%M"
    
    # If the string input is not valid, pass it through
    if not timestamp:
        return timestamp
    
    # Otherwise, convert to a datetime object and return
    return timestamp.strftime(format)


def get_number_of_records_for_user(user: models.User | int) -> int:
    """Gets the number of records for the specified user.
    
    The `user` input can be the user object or the user id.
    """

    # Extract the user id from the input
    user_id = user if isinstance(user, int) else user.user_id
    # Get the count of all records for the provided user
    return models.Record.query.filter_by(user_id=user_id).count()


def get_all_records_for_user(user: models.User | int) -> pd.DataFrame:
    """Gets all records for the provided user and returns as a dataframe.
    
    The `user` input can be the user object or the user id.
    """

    # Extract the user id from the input
    user_id = user if isinstance(user, int) else user.user_id
    # Get all of the records for the provided user
    records = models.Record.query.filter_by(user_id=user_id)
    records = [record.__dict__ for record in records.all()]
    # Convert the data to a dataframe
    df = pd.DataFrame.from_records(records)
    # Drop the instance state column
    df = df.drop(columns=["_sa_instance_state"])
    # Return the dataframe
    return df


def get_current_user_id() -> int | None:
    """Gets the user id of the currently signed in user."""
    return session.get("user_id", None)


def get_current_user() -> models.User | None:
    """Gets the currently signed in user."""
    user_id = session.get("user_id", None)
    return get_user_from_id(user_id)


def login_required(redirect_location: str=None) -> Callable:

    def decorator(original) -> Callable:
        nonlocal redirect_location

        # Set a default redirect location if none was provided
        if not redirect_location:
            redirect_location = "/login"
        
        @wraps(original)
        def wrapper(*args, **kwargs) -> Any | Response:
            """Wrapper to check that the user is logged in."""

            # Confirm that the user is logged in
            if not session.get("user_id", None):
                return redirect(redirect_location)

            # If there were no issues decoding, execute the wrapped function
            return original(*args, **kwargs)

        # Return the decorated function
        return wrapper
    
    # Return the actual decorator
    return decorator