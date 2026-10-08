import sqlite3

DB_NAME = "smartpark.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Initialize the parking spaces table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS parking_spaces (
                spot_number TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT 'available'
            )
            """
        )

        #Parking Sessions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_plate TEXT NOT NULL,
                space_id TEXT NOT NULL,
                entry_time TEXT NOT NULL,
                exit_time TEXT,
                fee REAL DEFAULT 0.0,
                fee_type TEXT NOT NULL, DEFAULT 'hourly',
                status TEXT NOT NULL DEFAULT 'active',
                FOREIGN KEY (space_id) REFERENCES parking_spaces(space_id)
            )
        """
        )
        conn.commit()