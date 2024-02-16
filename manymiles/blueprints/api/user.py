from flask import jsonify, make_response, Response
from flask_restful import Resource

from ...extensions import db
from ...models import User


class UserIDAPI(Resource):
    """API endpoint for getting's a user's ID from their username."""

    def get(self, username: str) -> Response:
        """Handles GET requests for the API endpoint."""

        # Abort if no username was supplied
        if not username:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "No username was supplied",
            }), 400)
        
        # Get the user object
        user = db.session.query(User).filter_by(username=username).first()

        # Check that the user actually exists
        if not user:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "No user exists with that username",
            }), 404)
        
        # Otherwise, return the ID of the user
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "User ID successfully retrieved",
            "data": {
                "username": user.username,
                "id": user.user_id,
            },
        }), 200)
