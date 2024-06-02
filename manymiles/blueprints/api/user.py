"""
Contains code for all user-related API endpoints.
"""


import datetime as dt

from flask import jsonify, make_response, request, Response
from flask_restful import Resource, reqparse
from sqlalchemy import func

from .validate import requires_admin, token_required
from ... import utilities
from ...extensions import db
from ...models import Role, User
from ...utilities import get_role_by_name, get_roles, log_api_request


def get_user_payload(user: User) -> dict:
    """Converts a user object to a json-serializable dictionary."""
    return {
        "id": user.user_id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


class UserAPI(Resource):
    """API endpoint for getting the authenticated user's ID."""

    @token_required
    def get(self, **kwargs) -> Response:
        """Handles GET requests for the API endpoint."""

        # Initialize the status for the response
        status = 200

        # Get the current user
        user = kwargs["current_user"]
        
        # Record the API request in the appropriate table
        log_api_request(user, request, status)

        # Otherwise, return the ID of the user
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "User ID successfully retrieved",
            "data": get_user_payload(user),
        }), status)
    
    @token_required
    @requires_admin
    def put(self, **kwargs) -> Response:
        """Handles PUT requests for the API endpoint."""

        # Initialize the status for the response
        status = 200

        # Get the current user
        user = kwargs["current_user"]
        
        # Set up a request parser object
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            type=str,
            help="Username of the new user",
            required=True,
        )
        parser.add_argument(
            "password",
            type=str,
            help="Password of the new user",
            required=True,
        )
        parser.add_argument(
            "email",
            type=str,
            help="Email of the new user",
            required=True,
        )
        parser.add_argument(
            "first_name",
            type=str,
            help="First name of the new user",
            required=False,
        )
        parser.add_argument(
            "last_name",
            type=str,
            help="Last name of the new user",
            required=False,
        )
        parser.add_argument(
            "role",
            type=str,
            help="Role name of the new user",
            required=False,
        )

        # Parse the arguments
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        email = args["email"]
        first_name = args["first_name"]
        last_name = args["last_name"]
        role = args["role"]

        # Set default values where appropriate
        if not role:
            role = "User"

        # Check if the provided email is valid
        if not utilities.is_valid_email(email):
            # Change the response code
            status = 400
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The provided email is invalid.",
            }), status)
        
        # Check if the provided username is valid
        if not utilities.is_valid_username(username):
            # Change the response code
            status = 400
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The provided username is invalid.",
            }), status)
        
        # Check if the provided username is available
        if not utilities.is_username_available(username):
            # Change the response code
            status = 400
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The provided username is not available.",
            }), status)
        
        # Check if the provided password is valid
        if not utilities.is_valid_password(password):
            # Change the response code
            status = 400
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The provided password is invalid.",
            }), status)
        
        # Check if the provided role id is valid
        valid_roles = get_roles()
        if not role in valid_roles:
            # Change the response code
            status = 400
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": f"The provided role must be one of: {valid_roles}.",
            }), status)

        # Create the user
        hash, salt = utilities.generate_hash(password)
        new_user = User(
            username=username,
            password_salt=salt,
            email=email,
            first_name=first_name,
            last_name=last_name,
            created=dt.datetime.now(),
            role_id=get_role_by_name(role).role_id,
        )

        # Add the user to the database
        utilities.create_account(new_user, hash)

        # Record the API request in the appropriate table
        log_api_request(user, request, status)

        # Return the response
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "User successfully created",
            "data": get_user_payload(new_user),
        }), status)
    
    @token_required
    @requires_admin
    def delete(self, **kwargs) -> Response:
        """Handles DELETE requests for the API endpoint."""

        # Initialize the status for the response
        status = 200

        # Get the current user
        user = kwargs["current_user"]
        
        # Set up a request parser object
        parser = reqparse.RequestParser()
        parser.add_argument(
            "user_id",
            type=int,
            help="User ID of the new user",
            location="args",
            required=False,
        )

        # Parse the arguments
        args = parser.parse_args()
        user_id = args["user_id"]

        # Use the provided id to get the associated user
        target_user = utilities.get_user_from_id(user_id)

        # Check if the user exists
        if not target_user:
            # Change the response code
            status = 404
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The user id does not have an associated account.",
            }), status)

        # Add the user to the database
        utilities.delete_account(target_user)

        # Record the API request in the appropriate table
        log_api_request(user, request, status)

        # Return the response
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "User successfully deleted",
            "data": get_user_payload(target_user),
        }), status)