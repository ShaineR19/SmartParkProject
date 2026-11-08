
from datetime import datetime
from backend.database import DatabaseManager
from backend.payment_service import PaymentService


class ParkingService:

    def __init__(self, database: DatabaseManager):
        self.database = database

    # Register a vehicle and assign a parking space
    def register_vehicle(self, license_plate):

        license_plate = license_plate.strip().upper()

        if not license_plate:
            raise ValueError("License plate cannot be empty.")

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
                    raise ValueError("This vehicle is already parked.")

            else:
                cursor = conn.execute(
                    """
                    INSERT INTO vehicles (license_plate)
                    VALUES (?)
                    """,
                    (license_plate,)
                )

                vehicle_id = cursor.lastrowid

            space = conn.execute(
                """
                SELECT * FROM parking_spaces
                WHERE status = 'AVAILABLE'
                ORDER BY space_number
                LIMIT 1
                """
            ).fetchone()

            if not space:
                raise ValueError("Parking lot is full.")

            space_id = space["space_id"]
            space_number = space["space_number"]

            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'ASSIGNED'
                WHERE space_id = ?
                """,
                (space_id,)
            )

            entry_time = datetime.now()

            cursor = conn.execute(
                """
                INSERT INTO parking_sessions (
                    vehicle_id,
                    space_id,
                    entry_time,
                    status
                )
                VALUES (?, ?, ?, 'ACTIVE')
                """,
                (vehicle_id, space_id, entry_time.isoformat())
            )

            conn.commit()

            return {
                "session_id": cursor.lastrowid,
                "vehicle_id": vehicle_id,
                "license_plate": license_plate,
                "space_id": space_id,
                "space_number": space_number,
                "entry_time": entry_time
            }

    # Mark an assigned space as occupied
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
                raise ValueError("Parking space does not exist.")

            if space["status"] != "ASSIGNED":
                raise ValueError("Parking space must be assigned first.")

            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'OCCUPIED'
                WHERE space_number = ?
                """,
                (space_number,)
            )

            conn.commit()

    # Get all parking spaces
    def get_all_spaces(self):

        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT space_id, space_number, status
                FROM parking_spaces
                ORDER BY space_number
                """
            ).fetchall()

        return [dict(row) for row in rows]

    # Get available spaces
    def get_available_spaces(self):

        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT space_id, space_number, status
                FROM parking_spaces
                WHERE status = 'AVAILABLE'
                ORDER BY space_number
                """
            ).fetchall()

        return [dict(row) for row in rows]

    # Get assigned spaces
    def get_assigned_spaces(self):

        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT space_id, space_number, status
                FROM parking_spaces
                WHERE status = 'ASSIGNED'
                ORDER BY space_number
                """
            ).fetchall()

        return [dict(row) for row in rows]

    # Get occupied spaces
    def get_occupied_spaces(self):

        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT space_id, space_number, status
                FROM parking_spaces
                WHERE status = 'OCCUPIED'
                ORDER BY space_number
                """
            ).fetchall()

        return [dict(row) for row in rows]

    # Get parking lot summary
    def get_lot_summary(self):

        with self.database.connect() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(*) AS total_spaces,
                    SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available_spaces,
                    SUM(CASE WHEN status = 'ASSIGNED' THEN 1 ELSE 0 END) AS assigned_spaces,
                    SUM(CASE WHEN status = 'OCCUPIED' THEN 1 ELSE 0 END) AS occupied_spaces
                FROM parking_spaces
                """
            ).fetchone()

        return {
            "total_spaces": row["total_spaces"] or 0,
            "available_spaces": row["available_spaces"] or 0,
            "assigned_spaces": row["assigned_spaces"] or 0,
            "occupied_spaces": row["occupied_spaces"] or 0
        }

    # Get active vehicles
    def get_active_vehicles(self):

        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    ps.session_id,
                    v.vehicle_id,
                    v.license_plate,
                    p.space_id,
                    p.space_number,
                    p.status AS space_status,
                    ps.entry_time
                FROM parking_sessions ps
                JOIN vehicles v
                    ON ps.vehicle_id = v.vehicle_id
                JOIN parking_spaces p
                    ON ps.space_id = p.space_id
                WHERE ps.status = 'ACTIVE'
                ORDER BY ps.entry_time
                """
            ).fetchall()

        return [dict(row) for row in rows]

    # Process vehicle checkout and payment
    def checkout_vehicle(self, license_plate, hourly_rate, parking_hours=None):

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
                raise ValueError("No active parking session found.")

            entry_time = datetime.fromisoformat(session["entry_time"])
            exit_time = datetime.now()

            if parking_hours is not None:
                duration = float(parking_hours)

                if duration <= 0:
                    raise ValueError("Parking duration must be greater than zero.")
            else:
                duration = PaymentService.calculate_duration(
                    entry_time,
                    exit_time
                )

            fee = PaymentService.calculate_fee(duration, hourly_rate)

            conn.execute(
                """
                UPDATE parking_sessions
                SET exit_time = ?,
                    status = 'COMPLETED'
                WHERE session_id = ?
                """,
                (exit_time.isoformat(), session["session_id"])
            )

            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'AVAILABLE'
                WHERE space_id = ?
                """,
                (session["space_id"],)
            )

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

            conn.commit()

            return {
                "transaction_id": cursor.lastrowid,
                "license_plate": license_plate,
                "space_number": session["space_number"],
                "entry_time": entry_time,
                "exit_time": exit_time,
                "duration_hours": duration,
                "payment_amount": fee
            }

    # Get payment transaction history
    def get_transactions(self):

        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    t.transaction_id,
                    v.license_plate,
                    p.space_number,
                    ps.entry_time,
                    ps.exit_time,
                    t.parking_duration,
                    t.payment_amount,
                    t.completed_at
                FROM transactions t
                JOIN parking_sessions ps
                    ON t.session_id = ps.session_id
                JOIN vehicles v
                    ON ps.vehicle_id = v.vehicle_id
                JOIN parking_spaces p
                    ON ps.space_id = p.space_id
                ORDER BY t.completed_at DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]
