from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Vehicle:
    license_plate: str
    vehicle_id: Optional[int] = None

@dataclass
class ParkingSpace:
    space_number: str
    status: str = 'AVAILABLE'
    space_id: Optional[int] = None

@dataclass
class ParkingSession:
    vehicle_id: int
    space_id: int
    entry_time: datetime
    session_id: Optional[int] = None
    exit_time: Optional[datetime] = None
    status: str = 'ACTIVE'

@dataclass
class Transaction:
    session_id: int
    parking_duration: float
    payment_amount: float
    completed_at: datetime
    transaction_id: Optional[int] = None
