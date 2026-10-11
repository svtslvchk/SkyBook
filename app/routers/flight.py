from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from uuid import UUID

from app.schemas.flight import FlightSchema
from app.exceptions.flight import FlightNotFound
from app.dependencies.flight import get_flight_service
from app.services.flight import FlightService


router = APIRouter(prefix="/api/v1/flights")


@router.get("", status_code=status.HTTP_200_OK,
            response_model=list[FlightSchema])
async def get_flights(
    flight_service: FlightService = Depends(get_flight_service)
) -> list[FlightSchema]:
    flights = await flight_service.get_all()
    return [FlightSchema.model_validate(f) for f in flights]


@router.get("/{flight_id}", status_code=status.HTTP_200_OK,
            response_model=FlightSchema)
async def get_flight(
    flight_id: UUID,
    flight_service: FlightService = Depends(get_flight_service)
) -> FlightSchema:
    try:
        flight = await flight_service.get_by_id(flight_id)
    except FlightNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рейс не найден."
        )
    return FlightSchema.model_validate(flight)
