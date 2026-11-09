# Libraries Used
import unittest
import tempfile
import sqlite3
from pathlib import Path
from datetime import datetime

# Files Used
from backend.database import DatabaseManager
from backend.parking_service import ParkingService
from backend.payment_service import PaymentService

class TestSmartPark(unittest.TestCase):
    # Create a temporary testing database
    def setUp(self):
        # SQLite in-memory
        db_uri = f"file:{self._testMethodName}?mode=memory&cache=shared"
        self.db = DatabaseManager(db_uri)
        self.db.initialize_database()
        self.parking = ParkingService(self.db)

    # Remove the temporary test database
    def tearDown(self):
        pass

    # UT-01: Parking Space Assignment
    def test_parking_space_assignment(self):
        # Add Parking Spaces
        self.db.add_parking_space("A1")
        self.db.add_parking_space("A2")

        # Make A1 OCCUPIED
        with self.db.connect() as conn:
            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'OCCUPIED'
                WHERE space_number = 'A1'
                """
            )
            
        # Register a vehicle
        result = self.parking.register_vehicle("ABC1234")
        self.assertEqual(result["space_number"], "A2")

        # Verify A1 is OCCUPIED
        with self.db.connect() as conn:
            a1 = conn.execute(
                """
                SELECT status FROM parking_spaces
                WHERE space_number = 'A1'
                """
            ).fetchone()
            
        self.assertEqual(a1["status"], "OCCUPIED")

    # UT-02: Parking Space Availability
    def test_parking_space_availability(self):
        # Add two parking spaces
        self.db.add_parking_space("A1")
        self.db.add_parking_space("A2")

        # Occupy every parking space
        with self.db.connect() as conn:
            conn.execute(
                """
                UPDATE parking_spaces
                SET status = 'OCCUPIED'
                """
            )
        
        # No available space should cause an error
        with self.assertRaisesRegex(
            ValueError, "Parking lot is full"
        ):self.parking.register_vehicle("ABC1234")

        # Verify no space was assigned
        available = self.parking.get_available_spaces()
        self.assertEqual(len(available), 0)

    # UT-03: Parking Fee Calculations
    def test_parking_fee_calculation(self):
        # Create Entry and Exit time and set Hourly Rate
        entry_time = datetime(2026, 11, 8, 8, 30)
        exit_time = datetime(2026, 11, 8, 12, 30)
        hourly_rate = 5.00

        # Calculate duration using Entry and Exit time
        duration = PaymentService.calculate_duration(
            entry_time, exit_time)
        
        # Calculate Hourly Rate 
        fee = PaymentService.calculate_fee(
            duration, hourly_rate)

        # Verify Duration and Fee
        self.assertEqual(duration, 4)
        self.assertEqual(fee, 20.00)

    # UT-04: Vehicle Registration
    def test_vehicle_registration(self):
        # Add Parking Space
        self.db.add_parking_space("A1")

        # Register New Vehicle
        license_plate = "ABC1234"
        self.parking.register_vehicle(license_plate)

        # Retrieve the vehicle from the database
        with self.db.connect() as conn:
            vehicle = conn.execute(
                """
                SELECT * FROM vehicles
                WHERE license_plate = ?
                """
                ,(license_plate,)
            ).fetchone()
            
        # Verify Vehicle is Registered
        self.assertIsNotNone(vehicle)
        self.assertEqual(
            vehicle["license_plate"],
            license_plate)

    # UT-05: Vehicle Exit
    def test_vehicle_exit(self):
        # Add Parking Space
        self.db.add_parking_space("A1")

        # Register a vehicle and assign A1
        result = self.parking.register_vehicle("ABC1234")

        # Mark the space as occupied
        self.parking.mark_space_occupied(
            result["space_number"])
        
        # Process the vehicle's exit
        self.parking.checkout_vehicle(
            license_plate="ABC1234",
            hourly_rate=5.00,
        )
        
        # Verify parking space becomes available
        with self.db.connect() as conn:
            space = conn.execute(
                """
                SELECT status FROM parking_spaces
                WHERE space_number = 'A1'
                """
            ).fetchone()
        self.assertEqual(space["status"], "AVAILABLE")


    # UT-06: Duplicate Vehicle Registration
    def test_duplicate_vehicle_registration(self):
        # Add Parking Spaces
        self.db.add_parking_space("A1")
        self.db.add_parking_space("A2")

        # Register the first vehicle
        self.parking.register_vehicle("ABC1234")

        # Attempt to register the same vehicle again
        try:
            self.parking.register_vehicle("ABC1234")
        except (ValueError, sqlite3.IntegrityError):
            pass

        # Verify only one active parking session exists
        with self.db.connect() as conn:
            count = conn.execute(
                """
                SELECT COUNT(*)
                FROM parking_sessions ps
                JOIN vehicles v ON ps.vehicle_id = v.vehicle_id
                WHERE v.license_plate = ?
                AND ps.status = 'ACTIVE'
                """,("ABC1234",)
            ).fetchone()[0]

        self.assertEqual(count, 1)


    # UT-07: Duplicate Parking Space
    def test_duplicate_parking_space(self):

        self.db.add_parking_space("A1")

        # Attempt to add the same space again
        try:
            self.db.add_parking_space("A1")
        except sqlite3.IntegrityError:
            pass

        with self.db.connect() as conn:
            count = conn.execute(
                """
                SELECT COUNT(*)
                FROM parking_spaces
                WHERE space_number = ?
                """, ("A1",)
            ).fetchone()[0]

        self.assertEqual(count, 1)


    # UT-08: Exit Without Active Session
    def test_exit_without_active_session(self):

        self.db.add_parking_space("A1")

        # No vehicle has been registered or parked
        with self.assertRaises(ValueError):
            self.parking.checkout_vehicle(
            license_plate="ABC1234",
            hourly_rate=5.00
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
