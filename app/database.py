"""Module responsible for configuration of the database connection"""
# pylint: disable=too-few-public-methods

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseConnection:
    """Class for creating a database session"""

    @staticmethod
    @contextmanager
    def connection() -> Session:
        """Create and yield a session"""
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()


class Connection(BaseConnection):
    """Additional class that inherits from BaseConnection made for testing with pytest"""


def get_session(func):
    """Decorator for providing a session"""

    def wrapper(*args):
        with Connection.connection() as session:
            return func(*args, session=session)
    return wrapper
