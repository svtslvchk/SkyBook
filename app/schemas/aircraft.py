from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class AircraftSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    airline_id: UUID
    model: str
    registration_number: str
    seat_capacity: int
    created_at: datetime


class AircraftCreateSchema(BaseModel):
    airline_id: UUID
    model: str
    registration_number: str
    seat_capacity: int


class AircraftUpdateSchema(BaseModel):
    airline_id: UUID | None = None
    model: str | None = None
    registration_number: str | None = None
    seat_capacity: int | None = None
