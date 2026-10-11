from enum import Enum


class FlightStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"
