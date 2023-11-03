from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
     
    __tablename__ = "user"

    user_id = Column("id", Integer, primary_key=True)
    username = Column("username", String(32), nullable=False)
    password = Column("password", String(64), nullable=False)
    email = Column("email", String(319), nullable=False)
    first_name = Column("first_name", String(35), nullable=True)
    last_name = Column("last_name", String(35), nullable=True)
    created = Column("created", DateTime, nullable=True)

    def __repr__(self) -> str:
        return ("User("
            f"user_id={repr(self.user_id)}, "
            f"username={repr(self.username)}, "
            f"password={repr(self.password)}, "
            f"email={repr(self.email)}, "
            f"first_name={repr(self.first_name)}, "
            f"last_name={repr(self.last_name)}"
            f"created={repr(self.created)}"
        ")")


class Record(Base):

    __tablename__ = "record"

    record_id = Column("id", Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    mileage = Column("mileage", Integer, nullable=False)
    recorded_datetime = Column("recorded_datetime", Integer, nullable=False)
    notes = Column("notes", String, nullable=True)

    def __repr__(self) -> str:
        return ("Record("
            f"record_id={repr(self.record_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"mileage={repr(self.mileage)}, "
            f"recorded_datetime={repr(self.recorded_datetime)}, "
            f"notes={repr(self.notes)}"
        ")")