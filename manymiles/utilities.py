import datetime as dt
import hashlib
import os
import re
from typing import Optional

from sqlalchemy.orm.session import Session

from .extensions import db
from . import models


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

    # Hash and salt the provided password
    h = hashlib.new("SHA256")
    h.update(user.password_salt + password_to_verify.encode())

    # Compare the two hashes and return the result
    return (user.password_hash == h.hexdigest())


def log_current_password(user: models.User) -> None:
    """Adds the user's current password to the password history table.
    
    Also updates the `password_id` column of the User record.

    Should be called after the user's password is updated and committed.
    """

    # 
    password = models.Password(
        user_id=user.user_id,
        password_hash=user.password_hash,
        updated_datetime=dt.datetime.now(),
    )
    db.session.add(password)
    db.session.commit()

    # 
    user.password_id = password.password_id
    db.session.commit()


def log_login(user: models.User) -> None:
    """Records the user's successful login in the login history table."""

    # Add the login to the database
    login = models.Login(
        user_id=user.user_id,
        login_datetime=dt.datetime.now(),
    )
    db.session.add(login)
    db.session.commit()


def create_account(user: models.User) -> models.User:
    """Creates an account and adds it to the database.
    
    Also adds a record to the password history table.
    """

    # Create a User object and add it to the database
    db.session.add(user)
    db.session.commit()

    # Log their password in the password history table
    log_current_password(user)

    # Log the user's successful login to the database
    log_login(user)


def is_username_available(username: str) -> bool:
    """Checks whether or not the provided username is available."""
    
    # See if there are any matches for the username in the database
    matches = db.session.query(models.User.user_id).filter_by(username=username)
    # If the username is available, there should have been no match
    return matches.first() is None


def is_valid_email(email: str) -> bool:
    """Checks whether or not the provided email is valid."""
    
    # TODO: Find better way
    expression = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return bool(re.match(expression, email))


def is_valid_password(password: str) -> bool:
    """Checks whether or not the provided password is valid.
    
    The password must be at least 7 characters long and include one lowercase
    letter, one uppercase letter, one number, and one special character.
    """
    
    expression = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{7,}$"
    return bool(re.match(expression, password))