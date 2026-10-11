from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.dependencies.aircraft import get_aircraft_service
from app.schemas.aircraft import (
    AircraftCreateSchema, AircraftUpdateSchema, AircraftSchema
)
from app.services.aircraft import AircraftService
from app.exceptions.aircraft import (
    NonExsistentAirline, AircraftHasFlightsError,
    AircraftNotFound
)


router = APIRouter(prefix="/api/v1/admin/aircrafts")


@router.post("", status_code=status.HTTP_201_CREATED,
             response_model=AircraftSchema)
async def create_aircraft(
        payload: AircraftCreateSchema,
        aircraft_service: AircraftService = Depends(get_aircraft_service)
) -> AircraftSchema:
    try:
        new_aircraft = await aircraft_service.create(payload)
    except NonExsistentAirline:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Самолет не может принадлежать несуществующей" +
            "авиакомпании."
        )

    return AircraftSchema.model_validate(new_aircraft)


@router.patch("/aircraft_id", status_code=status.HTTP_200_OK,
              response_model=AircraftSchema)
async def update_aircraft(
    aircraft_id: UUID,
    payload: AircraftUpdateSchema,
    aircraft_service: AircraftService = Depends(get_aircraft_service)
) -> AircraftSchema:
    try:
        aircraft = await aircraft_service.update(aircraft_id, payload)
    except NonExsistentAirline:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Самолет не может принадлежать несуществующей" +
            "авиакомпании."
        )
    except AircraftNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Самолет с id: {aircraft_id} не найден."
        )

    return AircraftSchema.model_validate(aircraft)


@router.delete("/aircraft_id", status_code=status.HTTP_200_OK,
               response_model=AircraftSchema)
async def delete_aircraft(
    aircraft_id: UUID,
    aircraft_service: AircraftService = Depends(get_aircraft_service)
) -> AircraftSchema:
    try:
        aircraft = await aircraft_service.delete(aircraft_id)
    except AircraftHasFlightsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя удалить аэропорт, участвующий в рейсах."
        )
    except AircraftNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Самолет с id: {aircraft_id} не найден."
        )
    return AircraftSchema.model_validate(aircraft)
