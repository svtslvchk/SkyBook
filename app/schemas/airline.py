from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class AirlineSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    iata_code: str
    created_at: datetime


class AirlineCreateSchema(BaseModel):
    name: str
    iata_code: str


class AirlineUpdateSchema(BaseModel):
    name: str | None = None
    iata_code: str | None = None
