from flask import jsonify, make_response, Response

from ...extensions import db
from ...models import User
from ...utilities import is_correct_password


def authenticate_user(
    username: str,
    password: str,
) -> tuple[bool, User | Response]:
    """Authenticates a user using a username and password combination.
    
    Returns a tuple with the first value being whether or not the operation
    was successful, and the second value being the user object if the operation
    was successful or the response to return if the operation failed.
    """

    # Abort if no username or password was supplied
    if not username or not password:
        return False, make_response(jsonify({
            "code": "FAILED",
            "message": "A username and password must both be supplied",
        }), 400)

    # Get the user object
    user = db.session.query(User).filter_by(username=username).first()

    # Abort if the user does not exist
    if not user:
        return False, make_response(jsonify({
            "code": "FAILED",
            "message": "No user exists with that username",
        }), 404)

    # Abort if the user could not be authenticated
    if not is_correct_password(user, password):
        return False, make_response(jsonify({
            "code": "FAILED",
            "message": "Incorrect password",
        }), 404)
    
    # Otherwise, simply return that the operation was successful
    return True, user
    