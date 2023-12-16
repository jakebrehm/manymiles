import datetime as dt

from flask import Blueprint, Flask
from flask_restful import Api, Resource, reqparse

from ...extensions import db
from ...models import Record, User
from ...utilities import is_correct_password


blueprint_api = Blueprint(
    "api",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/api/static",
)


def create_api(app: Flask) -> None:
    """Creates the API instance so that it can be used from the main script.
    
    Encapsulating the contents of this function was required in order to avoid
    circular references/imports and trying to use an unavailable application
    context.
    """

    # Create the API instance
    api = Api(app)

    # Add the API resources
    api.add_resource(
        UserIDAPI,
        "/api/user_id/<string:username>"
    )
    api.add_resource(
        MostRecentRecordAPI,
        "/api/most_recent_record/<string:username>&<string:password>"
    )
    api.add_resource(
        AddRecordAPI,
        "/api/add_record"
    )


class UserIDAPI(Resource):
    """API endpoint for getting a user's ID."""

    def get(self, username: str) -> dict:
        """GET request for the API endpoint."""

        # Return nothing if no username or password was supplied
        if not username:
            return {}
        
        # Get the user object
        user = db.session.query(User).filter_by(username=username).first()

        # Check that the user exists
        if not user:
            return {}
        
        # Get the ID of the user
        return {
            "user_id": user.user_id,
        }


class MostRecentRecordAPI(Resource):
    """API endpoint for getting a user's most recent record."""

    def get(self, username: str, password: str) -> dict:
        """GET request for the API endpoint."""

        # Return nothing if no username or password was supplied
        if not username or not password:
            return {}
        
        # Get the user object
        user = db.session.query(User).filter_by(username=username).first()

        # Check that the user exists
        if not user:
            return {}
    
        # Check if the username/password combination is correct
        if not is_correct_password(user, password):
            return {}
        
        # Get the most recent record for the user
        most_recent_record = (
            db.session.query(Record)
            .filter_by(user_id=user.user_id)
            .order_by(Record.recorded_datetime.desc())
            .first()
        )
        return {
            "date": most_recent_record.recorded_datetime.strftime(r"%Y-%m-%d"),
            "time": most_recent_record.recorded_datetime.strftime(r"%H:%M"),
            "mileage": most_recent_record.mileage,
        }
    

class AddRecordAPI(Resource):
    """API endpoint for adding a record."""

    put_args = reqparse.RequestParser()
    put_args.add_argument("username", type=str, help="Username", required=True)
    put_args.add_argument("password", type=str, help="Password", required=True)
    put_args.add_argument("date", type=str, help="Date", required=False)
    put_args.add_argument("time", type=str, help="Time", required=False)
    put_args.add_argument("mileage", type=str, help="Mileage", required=True)

    def put(self) -> dict | reqparse.RequestParser:
        """PUT request for the API endpoint."""

        # Parse arguments of the API call
        args = self.put_args.parse_args()
        username = args["username"]
        password = args["password"]
        date = args["date"]
        time = args["time"]
        mileage = int(args["mileage"])

        # Parse or set default values for date and time
        now = dt.datetime.now()
        if date:
            date = dt.datetime.strptime(date, r"%Y-%m-%d").date()
        else:
            date = now.date()
        
        if time:
            time = dt.datetime.strptime(time, r"%H:%M").time()
        else:
            time = now.time()
        
        # Combine the date and time
        recorded_datetime = dt.datetime.combine(date, time)

        # Return nothing if no username or password was supplied
        if not username or not password:
            return {}
        
        # Get the user object
        user = db.session.query(User).filter_by(username=username).first()

        # Check that the user exists
        if not user:
            return {}
    
        # Check if the username/password combination is correct
        if not is_correct_password(user, password):
            return {}
        
        # Add the record
        db.session.add(Record(
            user_id=user.user_id,
            mileage=mileage,
            recorded_datetime=recorded_datetime,
            notes=None,
        ))
        db.session.commit()

        # Return the arguments
        return args