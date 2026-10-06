import sqlite3

DB_NAME = "smartpark.db"


def init_db():

    with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()
#Initialize the parking spaces table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_spaces (
            spot_number TEXT PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'available'
        )
    """)

    conn.commit()
    conn.close()