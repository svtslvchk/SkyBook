from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from uuid import UUID

from app.schemas.flight import (
    FlightSchema, FlightUpdateSchema, FlightCreateSchema
)
from app.dependencies.flight import get_flight_service
from app.services.flight import FlightService
from app.exceptions.flight import (
    AircraftNotBelongAirline,
    DepartureArrivalCoincidence,
    InvalidFlightTime,
    FlightNotFound,
    InvalidFlightStatus
)
from app.exceptions.airline import AirlineNotFound
from app.exceptions.airport import AirportNotFound
from app.exceptions.aircraft import AircraftNotFound


router = APIRouter(prefix="/api/v1/admin/flights")


@router.post("", status_code=status.HTTP_201_CREATED,
             response_model=FlightSchema)
async def create_flight(
    payload: FlightCreateSchema,
    flight_service: FlightService = Depends(get_flight_service)
) -> FlightSchema:
    try:
        new_flight = await flight_service.create(payload)
    except AirlineNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанная авиакомпания не найдена."
        )
    except AircraftNotFound as arcrft_nf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{arcrft_nf}"
        )
    except AirportNotFound as arpt_nf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{arpt_nf}"
        )
    except AircraftNotBelongAirline:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Самолет не принадлежит указанной авиакомпании."
        )
    except DepartureArrivalCoincidence as dep_arr_con:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{dep_arr_con}"
        )
    except InvalidFlightStatus as inv_fs:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{inv_fs}"
        )
    return FlightSchema.model_validate(new_flight)


@router.patch("/{flight_id}", status_code=status.HTTP_200_OK,
              response_model=FlightSchema)
async def update_flight(
    flight_id: UUID,
    payload: FlightUpdateSchema,
    flight_service: FlightService = Depends(get_flight_service)
) -> FlightSchema:
    try:
        flight = await flight_service.update(flight_id, payload)
    except FlightNotFound as fnf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{fnf}"
        )
    except AirlineNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанная авиакомпания не найдена."
        )
    except AircraftNotFound as arcrft_nf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{arcrft_nf}"
        )
    except AirportNotFound as arpt_nf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{arpt_nf}"
        )
    except AircraftNotBelongAirline:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Самолет не принадлежит указанной авиакомпании."
        )
    except DepartureArrivalCoincidence as dep_arr_con:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{dep_arr_con}"
        )
    except InvalidFlightTime as invd_ft:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{invd_ft}"
        )
    except InvalidFlightStatus as inv_fs:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{inv_fs}"
        )

    return FlightSchema.model_validate(flight)


@router.delete("/{flight_id}", status_code=status.HTTP_200_OK,
               response_model=FlightSchema)
async def delete_flight(
    flight_id: UUID,
    flight_service: FlightService = Depends(get_flight_service)
) -> FlightSchema:
    try:
        flight = await flight_service.delete(flight_id)
    except FlightNotFound as fnf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{fnf}"
        )

    return FlightSchema.model_validate(flight)
