import datetime as dt

import jwt
from flask import current_app, jsonify, make_response, Response
from flask_restful import Resource, reqparse

from .validate import authenticate_user


class AuthenticateAPI(Resource):
    """API endpoint for authenticating a user and getting an API token."""

    def post(self) -> Response:
        """Handles POST requests for the API endpoint."""

        # Set up a request parser object
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            type=str,
            help="Username of the user",
            required=True,
        )
        parser.add_argument(
            "password",
            type=str,
            help="Password of the user",
            required=True,
        )

        # Parse the arguments
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]

        # Authenticate the user
        success, result = authenticate_user(username, password)

        # If the user failed to authenticate, return appropriate response
        if not success:
            return make_response(jsonify({
                    "code": "FAILED",
                    "message": "Authentication failed",
                }), 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})
        
        # Generate the expiration date and create the token
        expiration_datetime = dt.datetime.utcnow() + dt.timedelta(days=1)
        token = jwt.encode(
            payload={
                "user": username,
                "user_id": result.user_id,
                "exp": expiration_datetime,
            },
            key=current_app.config["SECRET_KEY"],
        )
        
        # Return the token to the user
        return make_response(jsonify({
            "code": "SUCCESS",
            "token": token,
        }), 200)
