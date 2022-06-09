import database

with database.connection() as conn:
    conn.execute("")
