from contextlib import contextmanager
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'database.db')


@contextmanager
def connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()


def get_db(func):
    def wrapper(*args):
        with connection() as cursor:
            return func(cursor, *args)
    return wrapper
