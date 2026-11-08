
from pathlib import Path
import sqlite3

class DatabaseManager:

    def __init__(self, db_path=None):

        if db_path is None:
            project_folder = Path(__file__).resolve().parent.parent
            db_path = project_folder / "data" / "smart_park.db"

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
                    license_plate TEXT UNIQUE NOT NULL,
                    vehicle_name TEXT
                )
            """)

            # Add vehicle_name to an existing database if needed
            columns = [
                column["name"]
                for column in conn.execute(
                    "PRAGMA table_info(vehicles)"
                ).fetchall()
            ]

            if "vehicle_name" not in columns:
                conn.execute(
                    "ALTER TABLE vehicles ADD COLUMN vehicle_name TEXT"
                )

            conn.execute("""
                CREATE TABLE IF NOT EXISTS parking_spaces (
                    space_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    space_number TEXT UNIQUE NOT NULL,
                    status TEXT NOT NULL DEFAULT 'AVAILABLE',
                    CHECK (status IN ('AVAILABLE','ASSIGNED','OCCUPIED'))
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
                    CHECK (status IN ('ACTIVE','COMPLETED')),
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
                    FOREIGN KEY (space_id) REFERENCES parking_spaces(space_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER UNIQUE NOT NULL,
                    parking_duration REAL NOT NULL,
                    payment_amount REAL NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES parking_sessions(session_id)
                )
            """)
            # Users table for permanent login accounts
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL
                 )
            """)
            conn.commit()

    def add_parking_space(self, space_number):

        with self.connect() as conn:

            try:
                conn.execute("""
                    INSERT INTO parking_spaces (space_number, status)
                    VALUES (?, 'AVAILABLE')
                """, (space_number,))

                conn.commit()

            except sqlite3.IntegrityError:
                print(f"Parking space {space_number} already exists.")
