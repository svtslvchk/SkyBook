from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.dependencies.aircraft import get_aircraft_service
from app.schemas.aircraft import AircraftSchema
from app.services.aircraft import AircraftService
from app.exceptions.aircraft import AircraftNotFound


router = APIRouter(prefix="/api/v1/aircrafts")


@router.get("", status_code=status.HTTP_200_OK,
            response_model=list[AircraftSchema])
async def get_aircrafts(
    aircraft_service: AircraftService = Depends(get_aircraft_service)
) -> list[AircraftSchema]:
    aircrafts = await aircraft_service.get_all()
    return [AircraftSchema.model_validate(a) for a in aircrafts]


@router.get("/{aircraft_id}", status_code=status.HTTP_200_OK,
            response_model=AircraftSchema)
async def get_aircraft(
    aircraft_id: UUID,
    aircraft_service: AircraftService = Depends(get_aircraft_service)
):
    try:
        aircraft = await aircraft_service.get_by_id(aircraft_id)
    except AircraftNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Самолет с id: {aircraft_id} не найден."
        )
    return AircraftSchema.model_validate(aircraft)
