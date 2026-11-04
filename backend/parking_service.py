from datetime import datetime
from backend.database import DatabaseManager
from backend.payment_service import PaymentService

class ParkingService:
    def __init__(self, database: DatabaseManager):
        self.database = database

    def checkout_vehicle(
        self,
        license_plate,
        hourly_rate
    ):
        license_plate = license_plate.strip().upper()

        with self.database.connect() as conn:

            session = conn.execute(
            """
            SELECT
                ps.session_id,
                ps.entry_time,
                ps.space_id,
                p.space_number
            FROM parking_sessions ps

            JOIN vehicles v
                ON ps.vehicle_id = v.vehicle_id

            JOIN parking_spaces p
                ON ps.space_id = p.space_id

            WHERE v.license_plate = ?
            AND ps.status = 'ACTIVE'
            """,
            (license_plate,)
        ).fetchone()

        if not session:
            raise ValueError(
                "No active parking session found."
            )

        entry_time = datetime.fromisoformat(
            session["entry_time"]
        )

        exit_time = datetime.now()

        duration = PaymentService.calculate_duration(
            entry_time,
            exit_time
        )

        fee = PaymentService.calculate_fee(
            duration,
            hourly_rate
        )

        # Complete the parking session

        conn.execute(
            """
            UPDATE parking_sessions
            SET exit_time = ?,
                status = 'COMPLETED'
            WHERE session_id = ?
            """,
            (
                exit_time.isoformat(),
                session["session_id"]
            )
        )

        # Release parking space

        conn.execute(
            """
            UPDATE parking_spaces
            SET status = 'AVAILABLE'
            WHERE space_id = ?
            """,
            (session["space_id"],)
        )

        # Save transaction

        cursor = conn.execute(
            """
            INSERT INTO transactions (
                session_id,
                parking_duration,
                payment_amount,
                completed_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                session["session_id"],
                duration,
                fee,
                exit_time.isoformat()
            )
        )

        transaction_id = cursor.lastrowid

        conn.commit()

        return {
            "transaction_id": transaction_id,
            "license_plate": license_plate,
            "space_number": session["space_number"],
            "entry_time": entry_time,
            "exit_time": exit_time,
            "duration_hours": duration,
            "payment_amount": fee,
        }

    def register_vehicle(
        self,
        license_plate
    ):
        license_plate = license_plate.strip().upper()

        if not license_plate:
            raise ValueError(
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