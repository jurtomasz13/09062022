from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

from . import config

DB = 'database.db'
TEST = 'test.db'


DB_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), TEST if config.TEST else DB)

DB_URL = f'sqlite:///{DB_PATH}'

print(DB_URL)


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


@contextmanager
def connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db(func):
    def wrapper(*args):
        with connection() as cursor:
            return func(cursor, *args)
    return wrapper
