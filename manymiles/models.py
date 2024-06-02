"""
Contains all models for the application's database.
"""


from flask_admin.contrib.sqla import ModelView
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, inspect, Integer, LargeBinary,
    String, Text,
)

from .extensions import admin, db


class User(db.Model):
     
    __tablename__ = "user"

    user_id = Column("id", Integer, primary_key=True)
    username = Column("username", String(32), nullable=False, unique=True)
    password_id = Column(
        "password_id",
        ForeignKey("password.id", name="fk_user_password"),
        nullable=True,
    )
    password_salt = Column("password_salt", LargeBinary, nullable=False)
    email = Column("email", String(319), nullable=False)
    first_name = Column("first_name", String(35), nullable=True)
    last_name = Column("last_name", String(35), nullable=True)
    created = Column("created", DateTime, nullable=True)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"user_id={repr(self.user_id)}, "
            f"username={repr(self.username)}, "
            f"password_id={repr(self.password_id)}, "
            f"password_salt={repr(self.password_salt)}, "
            f"email={repr(self.email)}, "
            f"first_name={repr(self.first_name)}, "
            f"last_name={repr(self.last_name)}, "
            f"created={repr(self.created)}"
        ")")


class Record(db.Model):

    __tablename__ = "record"

    record_id = Column("id", Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("user.id", name="fk_record_user"),
        nullable=False,
    )
    mileage = Column("mileage", Integer, nullable=False)
    record_datetime = Column("record_datetime", DateTime, nullable=False)
    create_datetime = Column("create_datetime", DateTime, nullable=True)
    update_datetime = Column("update_datetime", DateTime, nullable=True)
    notes = Column("notes", Text, nullable=True)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"record_id={repr(self.record_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"mileage={repr(self.mileage)}, "
            f"record_datetime={repr(self.record_datetime)}, "
            f"create_datetime={repr(self.create_datetime)}, "
            f"update_datetime={repr(self.update_datetime)}, "
            f"notes={repr(self.notes)}"
        ")")


class Login(db.Model):

    __tablename__ = "login"

    login_id = Column("id", Integer, primary_key=True)
    user_id = Column(
        "user_id",
        ForeignKey("user.id", name="fk_login_user"),
        nullable=False,
    )
    login_datetime = Column("login_datetime", DateTime, nullable=False)
    successful = Column("successful", Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"login_id={repr(self.login_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"login_datetime={repr(self.login_datetime)}"
        ")")


class Password(db.Model):

    __tablename__ = "password"

    password_id = Column("id", Integer, primary_key=True)
    user_id = Column(
        "user_id",
        ForeignKey("user.id", name="fk_password_user"),
        nullable=False,
    )
    password_hash = Column("password_hash", String(64), nullable=False)
    updated_datetime = Column("updated_datetime", DateTime, nullable=False)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"password_id={repr(self.password_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"password_hash={repr(self.password_hash)}, "
            f"updated_datetime={repr(self.updated_datetime)}"
        ")")


class Role(db.Model):

    __tablename__ = "role"

    role_id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"role_id={repr(self.role_id)}, "
            f"name={repr(self.name)}"
        ")")


class UserRole(db.Model):

    __tablename__ = "user_role"

    user_id = Column(
        "user_id",
        ForeignKey("user.id", name="fk_user_role_user"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        "role_id",
        ForeignKey("role.id", name="fk_user_role_role"),
        primary_key=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"user_id={repr(self.user_id)}, "
            f"role_id={repr(self.role_id)}"
        ")")


class ApiRequest(db.Model):

    __tablename__ = "api_request"

    request_id = Column("id", Integer, primary_key=True)
    user_id = Column(
        "user_id",
        ForeignKey("user.id", name="fk_api_request_user"),
        nullable=True,
    )
    endpoint = Column("endpoint", String(200), nullable=False)
    method = Column("method", String(30), nullable=False)
    status = Column("status", Integer, nullable=False)
    request_datetime = Column("request_datetime", DateTime, nullable=False)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"request_id={repr(self.request_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"endpoint={repr(self.endpoint)}, "
            f"method={repr(self.method)}, "
            f"status={repr(self.status)}, "
            f"request_datetime={repr(self.request_datetime)}"
        ")")


def get_columns(model) -> list:
    """Gets the list of columns from a model."""
    return [c_attr.key for c_attr in inspect(model).mapper.column_attrs]


# Create a child view to show primary keys and back references
class ChildView(ModelView):

    column_display_pk = True
    column_hide_backrefs = False

    def __init__(self,
        model,
        session,
        name=None,
        category=None,
        endpoint=None,
        url=None,
        **kwargs,
    ) -> None:
        """Initializes the ChildView class."""
        
        # Set any attributes passed as keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Initialize the instance using the parent's initialization method
        super(ChildView, self).__init__(
            model,
            session,
            name=name,
            category=category,
            endpoint=endpoint,
            url=url,
        )


def create_view(model, *args, **kwargs) -> ChildView:
    """Creates an instance of the ChildView."""
    return ChildView(
        model,
        db.session,
        *args,
        column_list=get_columns(model),
        **kwargs,
    )


# Add views for each model in the admin dashboard
admin.add_view(create_view(User))
admin.add_view(create_view(Record))
admin.add_view(create_view(Login, endpoint="login_"))
admin.add_view(create_view(Password))
admin.add_view(create_view(Role))
admin.add_view(create_view(UserRole))
admin.add_view(create_view(ApiRequest))