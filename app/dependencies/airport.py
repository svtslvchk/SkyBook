from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import get_db
from app.services.airport import AirportService


def get_airport_service(db: AsyncSession = Depends(get_db)) -> AirportService:
    return AirportService(db)
