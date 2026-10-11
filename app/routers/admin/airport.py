from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from app.schemas.airport import (
    AirportSchema, AirportCreateSchema, AirportUpdateSchema
)
from app.dependencies.airport import get_airport_service
from app.services.airport import AirportService
from app.exceptions.airport import (
    AirportHasFlightsError, AirportNotFound
)


router = APIRouter(prefix="/api/v1/admin/airports")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_airport(
    payload: AirportCreateSchema,
    airport_service: AirportService = Depends(get_airport_service)
) -> AirportSchema:
    new_airport = await airport_service.create(payload)
    return AirportSchema.model_validate(new_airport)


@router.patch("/{airport_id}", status_code=status.HTTP_200_OK)
async def update_airport(
    airport_id: UUID,
    payload: AirportUpdateSchema,
    airport_service: AirportService = Depends(get_airport_service)
) -> AirportSchema:
    try:
        airport_for_update = await airport_service.update(airport_id, payload)
    except AirportNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Аэропорт с id: {airport_id} не найден.'
        )

    return AirportSchema.model_validate(airport_for_update)


@router.delete("/{airport_id}", status_code=status.HTTP_200_OK)
async def delete_airport(
    airport_id: UUID,
    airport_service: AirportService = Depends(get_airport_service)
) -> AirportSchema:
    try:
        airport_for_delete = await airport_service.delete(airport_id)
    except AirportHasFlightsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя удалить аэропорт, у которого есть рейсы."
        )
    except AirportNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Аэропорт с id: {airport_id} не найден.'
        )

    return AirportSchema.model_validate(airport_for_delete)
