"""
Contains API-related helper functions.
"""


from functools import wraps
from typing import Any, Callable

import jwt
from flask import current_app, jsonify, make_response, Response, request

from ...extensions import db
from ...models import Role, User
from ...utilities import is_correct_password, log_api_request


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
        }), 401)

    # Abort if the user could not be authenticated
    if not is_correct_password(user, password):
        return False, make_response(jsonify({
            "code": "FAILED",
            "message": "Incorrect password",
        }), 401)
    
    # Otherwise, simply return that the operation was successful
    return True, user


def token_required(original) -> Callable:

    @wraps(original)
    def wrapper(*args, **kwargs) -> Any | Response:
        """Wraps the decorated function with a check for a valid API token."""

        # Abort if there was no token sent in the request json
        if not (token := request.headers.get("api-token")):
            return make_response(jsonify({
                "code": "FAILED",
                "message": "API token is missing.",
            }), 401)
        
        # If the token is able to be decoded, then the token is valid
        try:
            decoded = jwt.decode(
                jwt=token,
                key=current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
        # Abort if the token was not able to be decoded
        except jwt.DecodeError:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "API token is invalid.",
            }), 401)
        # Abort if the token has expired
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "API token signature has expired.",
            }), 401)
        # Abort if there was some other unhandled error
        except:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "Unhandled error occurred while decoding API token.",
            }), 400)
        
        # Get the current user from user id stored in the payload
        user_id = decoded["user_id"]
        current_user = User.query.filter_by(user_id=user_id).first()
        # Check that the user actually exists
        if not current_user:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "User associated with token could not be found.",
            }), 400)

        # If there were no issues decoding, execute the wrapped function
        return original(*args, **kwargs, current_user=current_user)

    # Return the decorated function
    return wrapper


def has_admin_rights(user: User, requires_owner: bool=False) -> bool:
    """Returns whether or not the user has admin rights."""
    return Role.query.filter_by(role_id=user.role_id).one().admin


def requires_admin(original) -> Callable:

    @wraps(original)
    def wrapper(*args, **kwargs) -> Any | Response:
        """Wrapper that checks for administrator permissions."""

        # Get the current user
        user = kwargs["current_user"]

        # Make sure the user has at least a minimum of admin rights
        if not has_admin_rights(user):
            # Change the response code
            status = 403
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": (
                    "You do not have the required permissions to perform this "
                    "action."
                ),
            }), status)
        
        # If there were no issues decoding, execute the wrapped function
        return original(*args, **kwargs)

    # Return the decorated function
    return wrapper