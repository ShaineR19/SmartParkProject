from pathlib import Path
import sqlite3

class DatabaseManager:
    def __init__(self, db_path="data/smart_park.db"):
        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        connection = sqlite3.connect(self.db_path)

        connection.row_factory = sqlite3.Row

        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def initialize_database(self):
        with self.connect() as conn:

            conn.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (

                    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_plate TEXT UNIQUE NOT NULL

                    )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS parking_spaces (

                    space_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    space_number TEXT UNIQUE NOT NULL,

                    status TEXT NOT NULL DEFAULT 'AVAILABLE',
                    CHECK (
                        status IN (
                            'AVAILABLE',
                            'ASSIGNED',
                            'OCCUPIED'

                            )
                        )
                    )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS parking_sessions (

                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    space_id INTEGER NOT NULL,
                    entry_time TEXT NOT NULL,
                    exit_time TEXT,

                    status TEXT NOT NULL DEFAULT 'ACTIVE',
                    CHECK (
                        status IN (
                            'ACTIVE',
                            'COMPLETED'
                        )
                    ),

                    FOREIGN KEY (vehicle_id)
                        REFERENCES vehicles(vehicle_id),

                    FOREIGN KEY (space_id)
                        REFERENCES parking_spaces(space_id)
                    )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (

                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER UNIQUE NOT NULL,
                    parking_duration REAL NOT NULL,
                    payment_amount REAL NOT NULL,
                    completed_at TEXT NOT NULL,
                    
                    FOREIGN KEY (session_id)
                        references parking_sessions(session_id)
                    )
            """)

            conn.commit()

    def add_parking_space(self, space_number):
        with self.connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO parking_spaces(
                    space_number,
                    status
                    )
                    values (?, 'AVAILABLE')
                    """,
                    (space_number,)
                )

                conn.commit()

            except sqlite3.IntegrityError:
                print(
                    f"Parking space {space_number} already exists."
                )