from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from app.schemas.airline import AirlineSchema
from app.dependencies.airline import get_service_airline
from app.services.airline import AirlineService
from app.exceptions.airline import AirlineNotFound


router = APIRouter(prefix="/api/v1/airlines", )


@router.get("", status_code=status.HTTP_200_OK,
            response_model=list[AirlineSchema])
async def get_airlines(
    service_airlines: AirlineService = Depends(get_service_airline)
) -> list[AirlineSchema]:
    airlines = await service_airlines.get_all()
    return [AirlineSchema.model_validate(a) for a in airlines]


@router.get("/{airline_id}", status_code=status.HTTP_200_OK,
            response_model=AirlineSchema)
async def get_airline(
    airline_id: UUID,
    service_airlines: AirlineService = Depends(get_service_airline)
) -> AirlineSchema:
    try:
        target_airline = await service_airlines.get_by_id(airline_id)
    except AirlineNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Авиакомпании с id: {airline_id} не найдено."
        )

    return AirlineSchema.model_validate(target_airline)
