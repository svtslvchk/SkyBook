from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.services.aircraft import AircraftService
from app.db.session import get_db


def get_aircraft_service(
        db: AsyncSession = Depends(get_db)) -> AircraftService:
    return AircraftService(db)
