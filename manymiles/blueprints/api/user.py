from flask import jsonify, make_response, Response
from flask_restful import Resource

from .validate import token_required
from ...models import User


class UserAPI(Resource):
    """API endpoint for getting the authenticated user's ID."""

    @token_required
    def get(self, **kwargs) -> Response:
        """Handles GET requests for the API endpoint."""

        # Get the current user
        user = kwargs["current_user"]
        
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
        }), 200)