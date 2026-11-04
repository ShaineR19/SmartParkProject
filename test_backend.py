from backend.database import DatabaseManager
from backend.parking_service import ParkingService


database = DatabaseManager()

database.initialize_database()


# Create some parking spaces

for number in [
    "A01",
    "A02",
    "A03",
    "A04",
    "A05"
]:
    database.add_parking_space(number)


parking = ParkingService(database)


print("\nRegistering vehicle...\n")

result = parking.register_vehicle(
    license_plate="ABC123",
)

print(result)


print("\nMarking space occupied...\n")

parking.mark_space_occupied(
    result["space_number"]
)


print("\nChecking vehicle out...\n")

transaction = parking.checkout_vehicle(
    license_plate="ABC123",
    hourly_rate=5.00
)

print(transaction)

print("\nLot Summary:\n")
print(parking.get_lot_summary())


print("\nAll Spaces:\n")

for space in parking.get_all_spaces():
    print(space)


print("\nActive Vehicles:\n")

for vehicle in parking.get_active_vehicles():
    print(vehicle)


print("\nTransactions:\n")

for transaction in parking.get_transactions():
    print(transaction)