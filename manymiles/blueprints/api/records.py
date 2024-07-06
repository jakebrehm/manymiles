"""
Contains code for all record-related API endpoints.
"""


import datetime as dt
from typing import Optional

from flask import jsonify, make_response, request, Response
from flask_restful import Resource, reqparse

from .validate import token_required
from ...extensions import db
from ...models import Record, User
from ...utilities import log_api_request, get_most_recent_record


def get_record_payload(
    record: Record,
    datetime_format: Optional[str] = None,
) -> dict:
    """Converts a record object to a json-serializable dictionary."""

    # Set a default value for the datetime format string
    if not datetime_format:
        datetime_format = r"%Y-%m-%d %H:%M"

    # Create the dictionary and return
    return {
        "mileage": record.mileage,
        "notes": record.notes,
        "recorded": record.record_datetime.strftime(datetime_format),
        "created": record.create_datetime.strftime(datetime_format),
        "updated": record.update_datetime.strftime(datetime_format),
    }


class MostRecentRecordAPI(Resource):
    """API endpoint for getting a user's most recent record."""

    @token_required
    def get(self, **kwargs) -> Response:
        """Handles GET requests for the API endpoint."""

        # Initialize the status for the response
        status = 200

        # Get the current user
        user = kwargs["current_user"]

        # Get the most recent record for the user
        record = get_most_recent_record(user)

        # Check if there are records to be retrieved
        if not record:
            # Change the response code
            status = 404
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The user has no records to retrieve."
            }), status)
        
        # Record the API request in the appropriate table
        log_api_request(user, request, status)
    
        # Return the metadata of the user's most recent record
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully retrieved",
            "data": get_record_payload(record),
        }), status)
    
    @token_required
    def delete(self, **kwargs) -> Response:
        """Handles DELETE requests for the API endpoint."""

        # Initialize the status for the response
        status = 200

        # Get the current user
        user = kwargs["current_user"]
        
        # Get the most recent record for the user
        record = get_most_recent_record(user)

        # Check if there are records to be deleted
        if not record:
            # Change the response code
            status = 404
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The user has no records to delete."
            }), status)
        
        # Delete the record from the database
        db.session.delete(record)
        db.session.commit()

        # Record the API request in the appropriate table
        log_api_request(user, request, status)

        # Return the response
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully deleted",
            "data": get_record_payload(record),
        }), status)


class RecordAPI(Resource):
    """API endpoint for creating or modifying records."""

    @token_required
    def post(self, **kwargs) -> Response:
        """Handles POST requests for the API endpoint."""

        # Initialize the status for the response
        status = 200

        # Get the current user
        user = kwargs["current_user"]

        # Set up a request parser object
        parser = reqparse.RequestParser()
        parser.add_argument(
            "mileage",
            type=int,
            help=(
                "A mileage value for the record is required to be sent in the "
                "body of the request as an integer"
            ),
            required=True,
        )
        parser.add_argument(
            "date",
            type=str,
            help=r"Date of the record should be specified in format %Y-%m-%d",
            required=False,
        )
        parser.add_argument(
            "time",
            type=str,
            help=r"Time of the record should be specified in format %H:%M",
            required=False,
        )
        parser.add_argument(
            "notes",
            type=str,
            help="Notes for the record should be supplied as a string",
            required=False,
        )

        # Parse the arguments
        args = parser.parse_args()
        mileage = args["mileage"]
        date = args["date"]
        time = args["time"]
        notes = args["notes"]

        # Abort if no mileage value was supplied
        if not mileage:
            # Change the response code
            status = 400
            # Record the API request in the appropriate table
            log_api_request(user, request, status)
            # Form and return the response
            return make_response(jsonify({
                "code": "FAILED",
                "message": "A mileage value must be supplied.",
            }), status)

        # Abort if provided date is invalid
        if date:
            try:
                dt.datetime.strptime(date, r"%Y-%m-%d")
            except:
                # Change the response code
                status = 400
                # Record the API request in the appropriate table
                log_api_request(user, request, status)
                # Form and return the response
                return make_response(jsonify({
                    "code": "FAILED",
                    "message": (
                        r"A valid date should be provided in format %Y-%m-%d."
                    ),
                }), status)

        # Abort if provided time is invalid
        if time:
            try:
                dt.datetime.strptime(time, r"%H:%M")
            except:
                # Change the response code
                status = 400
                # Record the API request in the appropriate table
                log_api_request(user, request, status)
                # Form and return the response
                return make_response(jsonify({
                    "code": "FAILED",
                    "message": (
                        r"A valid time should be provided in format %H:%M."
                    ),
                }), status)
        
        # Get the current datetime
        current_datetime = dt.datetime.now()

        # Parse or set default values for date and time
        if date:
            date = dt.datetime.strptime(date, r"%Y-%m-%d").date()
        else:
            date = current_datetime.date()
        
        if time:
            time = dt.datetime.strptime(time, r"%H:%M").time()
        else:
            time = current_datetime.time()
        
        # Combine the date and time
        record_datetime = dt.datetime.combine(date, time)

        # Create the new record
        new_record = Record(
            user_id=user.user_id,
            mileage=mileage,
            record_datetime=record_datetime,
            create_datetime=current_datetime,
            update_datetime=current_datetime,
            notes=notes if notes else None,
        )

        # Add the record to the database
        db.session.add(new_record)
        db.session.commit()

        # Record the API request in the appropriate table
        log_api_request(user, request, status)

        # Return the metadata of the newly created record
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully created",
            "data": get_record_payload(new_record),
        }), status)