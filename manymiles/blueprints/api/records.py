import datetime as dt

from flask import jsonify, make_response, Response
from flask_restful import Resource, reqparse

from .validate import authenticate_user
from ...extensions import db
from ...models import Record


class MostRecentRecordAPI(Resource):
    """API endpoint for getting a user's most recent record."""

    def get(self) -> Response:
        """Handles GET requests for the API endpoint."""

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
        if not success:
            return result

        # Get the most recent record for the user
        record = (
            db.session.query(Record)
            .filter_by(user_id=result.user_id)
            .order_by(Record.record_datetime.desc())
            .first()
        )

        # Return the metadata of the user's most recent record
        dt_format = r"%Y-%m-%d %H:%M"
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully retrieved",
            "data": {
                "mileage": record.mileage,
                "recorded": record.record_datetime.strftime(dt_format),
                "created": record.create_datetime.strftime(dt_format),
                "updated": record.update_datetime.strftime(dt_format),
            },
        }), 200)
    
    def delete(self) -> Response:
        """Handles DELETE requests for the API endpoint."""

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
        if not success:
            return result
        
        # Get the most recent record for the user
        record = (
            db.session.query(Record)
            .filter_by(user_id=result.user_id)
            .order_by(Record.record_datetime.desc())
            .first()
        )

        # Delete the record from the database
        db.session.delete(record)
        db.session.commit()

        # Return the metadata of the deleted record
        dt_format = r"%Y-%m-%d %H:%M"
        return make_response(jsonify({
            "code": "SUCCESS",
            "message": "Record successfully deleted",
            "data": {
                "mileage": record.mileage,
                "recorded": record.record_datetime.strftime(dt_format),
                "created": record.create_datetime.strftime(dt_format),
                "updated": record.update_datetime.strftime(dt_format),
            },
        }), 200)


class RecordAPI(Resource):
    """API endpoint for creating or modifying records."""

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
        parser.add_argument(
            "date",
            type=str,
            help="Date of the record",
            required=False,
        )
        parser.add_argument(
            "time",
            type=str,
            help="Time of the record",
            required=False,
        )
        parser.add_argument(
            "mileage",
            type=str,
            help="Mileage of the record",
            required=True,
        )
        parser.add_argument(
            "notes",
            type=str,
            help="Notes for the record",
            required=False,
        )

        # Parse the arguments
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        date = args["date"]
        time = args["time"]
        mileage = args["mileage"]
        notes = args["notes"]

        # Abort if no mileage value was supplied
        if not mileage:
            return make_response(jsonify({
                "code": "FAILED",
                "message": "A mileage value must be supplied",
            }), 400)

        # Authenticate the user
        success, result = authenticate_user(username, password)
        if not success:
            return result
        
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
            user_id=result.user_id,
            mileage=mileage,
            record_datetime=record_datetime,
            create_datetime=current_datetime,
            update_datetime=current_datetime,
            notes=notes if notes else None,
        ))
        db.session.commit()

        # Return the metadata of the user's most recent record
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