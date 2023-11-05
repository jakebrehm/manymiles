from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
     
    __tablename__ = "user"

    user_id = Column("id", Integer, primary_key=True)
    username = Column("username", String(32), nullable=False)
    password_id = Column(
        "password_id",
        ForeignKey("password.id", name="fk_user_password"),
        nullable=True,
    )
    password_hash = Column("password_hash", String(64), nullable=False)
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
            f"password_hash={repr(self.password_hash)}, "
            f"password_salt={repr(self.password_salt)}, "
            f"email={repr(self.email)}, "
            f"first_name={repr(self.first_name)}, "
            f"last_name={repr(self.last_name)}, "
            f"created={repr(self.created)}"
        ")")


class Record(Base):

    __tablename__ = "record"

    record_id = Column("id", Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("user.id", name="fk_record_user"),
        nullable=False,
    )
    mileage = Column("mileage", Integer, nullable=False)
    recorded_datetime = Column("recorded_datetime", DateTime, nullable=False)
    notes = Column("notes", Text, nullable=True)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"record_id={repr(self.record_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"mileage={repr(self.mileage)}, "
            f"recorded_datetime={repr(self.recorded_datetime)}, "
            f"notes={repr(self.notes)}"
        ")")


class Login(Base):

    __tablename__ = "login"

    login_id = Column("id", Integer, primary_key=True)
    user_id = Column(
        "user_id",
        ForeignKey("user.id", name="fk_login_user"),
        nullable=False,
    )
    login_datetime = Column("login_datetime", DateTime, nullable=False)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"login_id={repr(self.login_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"login_datetime={repr(self.login_datetime)}"
        ")")


class Password(Base):

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


class Role(Base):

    __tablename__ = "role"

    role_id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
            f"role_id={repr(self.role_id)}, "
            f"name={repr(self.name)}"
        ")")


class UserRole(Base):

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