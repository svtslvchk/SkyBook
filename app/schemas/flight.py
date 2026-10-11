from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.enums.flight import FlightStatus


class FlightSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    flight_number: str
    airline_id: UUID
    aircraft_id: UUID
    origin_airport_id: UUID
    destination_airport_id: UUID
    departure_at: datetime
    arrival_at: datetime
    status: FlightStatus
    created_at: datetime


class FlightCreateSchema(BaseModel):
    flight_number: str = Field(min_length=1, max_length=10)
    airline_id: UUID
    aircraft_id: UUID
    origin_airport_id: UUID
    destination_airport_id: UUID
    departure_at: datetime
    arrival_at: datetime
    status: FlightStatus = FlightStatus.SCHEDULED

    @model_validator(mode="after")
    def validate_flight(self):
        if self.origin_airport_id == self.destination_airport_id:
            raise ValueError("Аэропорты вылета и прилёта должны различаться")

        if self.arrival_at <= self.departure_at:
            raise ValueError("Время прилёта должно быть позже времени вылета")

        return self


class FlightUpdateSchema(BaseModel):
    flight_number: str | None = Field(
        default=None, min_length=1, max_length=10
    )
    airline_id: UUID | None = None
    aircraft_id: UUID | None = None
    origin_airport_id: UUID | None = None
    destination_airport_id: UUID | None = None
    departure_at: datetime | None = None
    arrival_at: datetime | None = None
    status: FlightStatus | None = None
