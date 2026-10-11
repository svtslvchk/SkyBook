from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.services.airline import AirlineService
from app.db.session import get_db


def get_service_airline(db: AsyncSession = Depends(get_db)) -> AirlineService:
    return AirlineService(db)
