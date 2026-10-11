from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from app.schemas.airline import (
    AirlineSchema, AirlineCreateSchema, AirlineUpdateSchema
)
from app.dependencies.airline import get_service_airline
from app.services.airline import AirlineService
from app.exceptions.airline import (
    AirlineHasAircraftError, NonUniqueIataCode,
    AirlineHasFlightError, AirlineNotFound
)


router = APIRouter(prefix="/api/v1/admin/airlines")


@router.post("", status_code=status.HTTP_201_CREATED,
             response_model=AirlineSchema)
async def create_airline(
    payload: AirlineCreateSchema,
    service_airline: AirlineService = Depends(get_service_airline)
) -> AirlineSchema:
    try:
        new_airline = await service_airline.create(payload)
    except NonUniqueIataCode:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="iata_code аэропорт должен быть уникальным."
        )
    return AirlineSchema.model_validate(new_airline)


@router.patch("/{airline_id}", status_code=status.HTTP_200_OK,
              response_model=AirlineSchema)
async def update_airline(
    airline_id: UUID,
    payload: AirlineUpdateSchema,
    service_airline: AirlineService = Depends(get_service_airline)
) -> AirlineSchema:
    try:
        airline_for_update = await service_airline.update(airline_id, payload)
    except AirlineNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Авиакомпании с id: {airline_id} не найдено."
        )

    return AirlineSchema.model_validate(airline_for_update)


@router.delete("/{airline_id}", status_code=status.HTTP_200_OK,
               response_model=AirlineSchema)
async def delete_airline(
    airline_id: UUID,
    service_airline: AirlineService = Depends(get_service_airline)

):
    try:
        airline_for_delete = await service_airline.delete(airline_id)
    except AirlineHasAircraftError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя удалить авиакомпанию, у которой есть самолеты."
        )
    except AirlineHasFlightError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя удалить авиакомпанию, у которой есть рейсы."
        )
    except AirlineNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Авиакомпании с id: {airline_id} не найдено."
        )

    return AirlineSchema.model_validate(airline_for_delete)
