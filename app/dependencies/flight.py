from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import get_db
from app.services.flight import FlightService


def get_flight_service(
        db: AsyncSession = Depends(get_db)
) -> FlightService:
    return FlightService(db)
