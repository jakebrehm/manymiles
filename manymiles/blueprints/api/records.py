import datetime as dt
from typing import Optional

from flask import jsonify, make_response, Response
from flask_restful import Resource, reqparse

from .validate import token_required
from ...extensions import db
from ...models import Record, User


class MostRecentRecordAPI(Resource):
    """API endpoint for getting a user's most recent record."""

    @token_required
    def get(self, **kwargs) -> Response:
        """Handles GET requests for the API endpoint."""

        # Get the current user
        user = kwargs["current_user"]

        # Get the most recent record for the user
        record = self.get_most_recent_record(user)

        # Abort if there are no records to be deleted
        if not record:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The user has no records to retrieve."
            }), 400)

        # Return the metadata of the user's most recent record
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully retrieved",
            "data": self.get_record_payload(record),
        }), 200)
    
    @token_required
    def delete(self, **kwargs) -> Response:
        """Handles DELETE requests for the API endpoint."""

        # Get the current user
        user = kwargs["current_user"]
        
        # Get the most recent record for the user
        record = self.get_most_recent_record(user)

        # Abort if there are no records to be deleted
        if not record:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "The user has no records to delete."
            }), 400)

        # Delete the record from the database
        db.session.delete(record)
        db.session.commit()

        # Return the metadata of the deleted record
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully deleted",
            "data": self.get_record_payload(record),
        }), 200)

    def get_most_recent_record(self, user: User) -> Record:
        """Gets the most recently recorded record of the provided user."""
        return (
            db.session.query(Record)
            .filter_by(user_id=user.user_id)
            .order_by(Record.record_datetime.desc())
            .first()
        )

    def get_record_payload(self,
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


class RecordAPI(Resource):
    """API endpoint for creating or modifying records."""

    @token_required
    def post(self, **kwargs) -> Response:
        """Handles POST requests for the API endpoint."""

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
            return make_response(jsonify({
                "code": "FAILED",
                "message": "A mileage value must be supplied",
            }), 400)
        
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

        # Create the record
        db.session.add(Record(
            user_id=user.user_id,
            mileage=mileage,
            record_datetime=record_datetime,
            create_datetime=current_datetime,
            update_datetime=current_datetime,
            notes=notes if notes else None,
        ))
        db.session.commit()

        # Return the metadata of the newly created record
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully created",
            "data": {
                "mileage": mileage,
                "notes": notes,
                "recorded": record_datetime,
                "created": current_datetime,
                "updated": current_datetime,
            },
        }), 200)