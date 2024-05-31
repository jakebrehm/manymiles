"""
Contains code for all user-related API endpoints.
"""


from flask import jsonify, make_response, request, Response
from flask_restful import Resource

from .validate import token_required
from ...utilities import log_api_request


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
            "data": {
                "id": user.user_id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }), status)