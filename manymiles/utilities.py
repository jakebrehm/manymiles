import hashlib
import os
from typing import Optional

import models


def generate_hash(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
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