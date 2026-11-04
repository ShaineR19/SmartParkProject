from datetime import datetime
from backend.database import DatabaseManager

class ParkingService:
    def __init__(self, database: DatabaseManager):
        self.database = database

    def register_vehicle(
        self,
        license_plate
    ):
        license_plate = license_plate.strip().upper()

        if not license_plate:
            raise Valueerror(
                "License plate cannot be empty."
            )

        with self.database.connect() as conn:
            vehicle = conn.execute(
                """
                SELECT * FROM vehicles
                WHERE license_plate = ?
                """,
                (license_plate,)
            ).fetchone()

            if vehicle:
                vehicle_id = vehicle["vehicle_id"]

                active_session = conn.execute(
                    """
                    SELECT * FROM parking_sessions
                    WHERE vehicle_id = ?
                    AND status = 'ACTIVE'
                    """,
                    (vehicle_id,)
                ).fetchone()

                if active_session:
                    raise ValueError(
                        "This vehicle is already parked."
                    )
            else:
                cursor = conn.execute(
                    """
                    INSERT INTO vehicles (
                        license_plate,
                        customer_name
                    )
                    VALUES (?, ?)
                    """,
                    (
                        license_plate,
                    )
                )

                vehicle_id = cursor.lastrowid

            space = conn.execute(
                """
                SELECT * FROM parking_spaces
                WHERE status = 'AVAILABLE'
                ORDER BY space_number
                limit 1
                """
            ).fetchone()

            if not space:
                raise ValueError(
                    "Parking lot is full."
                )

            space_id = space["space_id"]
            space_number = space["space_number"]

            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'ASSIGNED'
                WHERE space_id = ?
                """
                (space_id,)
            )

            entry_time = datetime.now()

            cursor.conn.execute(
                """
                INSERT INTO parking_sessions (
                    vehicle_id,
                    space_id,
                    entry_time,
                    status
                )
                VALUES (?, ?, ?, 'ACTIVE')
                """,
                (
                    vehicle_id,
                    space_id,
                    entry_time.isoformat()
                )
            )

            session_id = cursor.lastrowid

            conn.commit()
            return {
                "session_id": session_id,
                "vehicle_id": vehicle_id,
                "license_plate": license_plate,
                "space_id": space_id,
                "space_number": space_number,
                "entry_time": entry_time,
            }

    def mark_space_occupied(self, space_number):
        with self.database.connect() as conn:
            space = conn.execute(
                """
                SELECT * FROM parking_spaces
                WHERE space_number = ?
                """,
                (space_number,)
            ).fetchone()

            if not space:
                raise ValueError(
                    "Parking space does noe exist."
                )
            if space["status"] != "ASSIGNED":
                raise ValueError(
                    "Parking space must be assigned first."
                )
            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'OCCUPIED'
                WHERE space_number = ?
                """,
                (space_number,)
            )
            conn.commit()