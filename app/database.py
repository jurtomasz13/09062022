from contextlib import contextmanager
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'database.db')


@contextmanager
def connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    finally:
        conn.commit()
        conn.close()
