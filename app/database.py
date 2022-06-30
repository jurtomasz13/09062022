import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# @contextmanager
# def connection():
#     conn = sqlite3.connect(DB_PATH)
#     try:
#         yield conn.cursor()
#     finally:
#         conn.commit()
#         conn.close()


# @contextmanager
# def connection():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


class BaseConnection:
    @staticmethod
    @contextmanager
    def connection():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


class TestConnection(BaseConnection):
    pass


def get_db(func):
    def wrapper(*args):
        with TestConnection.connection() as cursor:
            return func(cursor, *args)

    return wrapper
