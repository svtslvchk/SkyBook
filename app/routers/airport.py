from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from app.schemas.airport import AirportSchema
from app.dependencies.airport import get_airport_service
from app.services.airport import AirportService
from app.exceptions.airport import AirportNotFound


router = APIRouter(prefix="/api/v1/airports")


@router.get("", status_code=status.HTTP_200_OK,
            response_model=list[AirportSchema])
async def get_airports(
    airport_service: AirportService = Depends(get_airport_service)
) -> list[AirportSchema]:
    airports = await airport_service.get_all()
    return [AirportSchema.model_validate(a) for a in airports]


@router.get("/{airport_id}", status_code=status.HTTP_200_OK,
            response_model=AirportSchema)
async def get_airport(
    airport_id: UUID,
    airport_service: AirportService = Depends(get_airport_service)
) -> AirportSchema:
    try:
        target_airport = await airport_service.get_by_id(airport_id)
    except AirportNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Аэропорт с id: {airport_id} не найден."
        )
    return AirportSchema.model_validate(target_airport)
