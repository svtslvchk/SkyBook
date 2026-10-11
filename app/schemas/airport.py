from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class AirportSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    iata_code: str
    name: str
    city: str
    country: str
    created_at: datetime


class AirportCreateSchema(BaseModel):
    iata_code: str
    name: str
    city: str
    country: str


class AirportUpdateSchema(BaseModel):
    iata_code: str | None = None
    name: str | None = None
    city: str | None = None
    country: str | None = None
