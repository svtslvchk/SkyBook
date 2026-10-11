from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.repositories.flight import FlightRepository
from app.models.flight import FlightORM
from app.schemas.flight import (
    FlightCreateSchema, FlightUpdateSchema
)
from app.repositories.aircraft import AircraftRepository
from app.repositories.airline import AirlineRepository
from app.repositories.airport import AirportRepository
from app.exceptions.airline import AirlineNotFound
from app.exceptions.airport import AirportNotFound
from app.exceptions.aircraft import AircraftNotFound
from app.exceptions.flight import (
    AircraftNotBelongAirline,
    DepartureArrivalCoincidence,
    InvalidFlightTime,
    FlightNotFound,
    InvalidFlightStatus
)
from app.enums.flight import FlightStatus


class FlightService:
    def __init__(self, db: AsyncSession):
        self.flight_repository = FlightRepository(db)
        self.airport_repository = AirportRepository(db)
        self.airline_repository = AirlineRepository(db)
        self.aircraft_repository = AircraftRepository(db)

    async def get_all(self) -> list[FlightORM]:
        return await self.flight_repository.get_all()

    async def get_by_id(self, flight_id: UUID) -> FlightORM | None:
        flight = await self.flight_repository.get_by_id(flight_id)
        if flight is None:
            raise FlightNotFound(
                "Рейса с id: {flight_id} не найдено."
            )
        return flight

    async def _validate_references(
        self,
        airline_id: UUID,
        aircraft_id: UUID,
        origin_airport_id: UUID,
        destination_airport_id: UUID,
    ) -> None:
        airline = await self.airline_repository.get_by_id(
            airline_id
        )
        if airline is None:
            raise AirlineNotFound(
                "Указанная авиакомпания не найдена."
            )

        aircraft = await self.aircraft_repository.get_by_id(
            aircraft_id
        )
        if aircraft is None:
            raise AircraftNotFound(
                "Указанный самолет не найден."
            )

        if aircraft.airline_id != airline_id:
            raise AircraftNotBelongAirline(
                "Самолет не принадлежит указанной авиакомпании."
            )

        origin = await self.airport_repository.get_by_id(
            origin_airport_id
        )
        if origin is None:
            raise AirportNotFound(
                "Аэропорт вылета не найден."
            )

        destination = await self.airport_repository.get_by_id(
            destination_airport_id
        )
        if destination is None:
            raise AirportNotFound(
                "Аэропорт прилета не найден."
            )

        if origin_airport_id == destination_airport_id:
            raise DepartureArrivalCoincidence(
                "Аэропорты вылета и прилета должны различаться."
            )

    def _validate_status(self, status: FlightStatus | None) -> None:
        if status is not None and not isinstance(status, FlightStatus):
            raise InvalidFlightStatus("Некорректный статус рейса.")

    async def create(self, payload: FlightCreateSchema) -> FlightORM:
        await self._validate_references(
            payload.airline_id,
            payload.aircraft_id,
            payload.origin_airport_id,
            payload.destination_airport_id,
        )

        self._validate_status(payload.status)

        new_flight = FlightORM(
            flight_number=payload.flight_number,
            airline_id=payload.airline_id,
            aircraft_id=payload.aircraft_id,
            origin_airport_id=payload.origin_airport_id,
            destination_airport_id=payload.destination_airport_id,
            departure_at=payload.departure_at,
            arrival_at=payload.arrival_at,
            status=payload.status.value,
        )

        return await self.flight_repository.create(new_flight)

    async def update(
            self, flight_id: UUID, payload: FlightUpdateSchema
    ) -> FlightORM | None:
        flight = await self.flight_repository.get_by_id(flight_id)
        if flight is None:
            raise FlightNotFound(
                "Рейса с id: {flight_id} не найдено."
            )

        airline_id = (
            payload.airline_id
            if payload.airline_id is not None
            else flight.airline_id
        )
        aircraft_id = (
            payload.aircraft_id
            if payload.aircraft_id is not None
            else flight.aircraft_id
        )
        origin_airport_id = (
            payload.origin_airport_id
            if payload.origin_airport_id is not None
            else flight.origin_airport_id
        )
        destination_airport_id = (
            payload.destination_airport_id
            if payload.destination_airport_id is not None
            else flight.destination_airport_id
        )
        departure_at = (
            payload.departure_at
            if payload.departure_at is not None
            else flight.departure_at
        )
        arrival_at = (
            payload.arrival_at
            if payload.arrival_at is not None
            else flight.arrival_at
        )

        await self._validate_references(
            airline_id,
            aircraft_id,
            origin_airport_id,
            destination_airport_id
        )

        if departure_at >= arrival_at:
            raise InvalidFlightTime(
                "Вылет не может быть позже прилета."
            )

        if payload.flight_number is not None:
            flight.flight_number = payload.flight_number

        flight.airline_id = airline_id
        flight.aircraft_id = aircraft_id
        flight.origin_airport_id = origin_airport_id
        flight.destination_airport_id = destination_airport_id
        flight.departure_at = departure_at
        flight.arrival_at = arrival_at

        if payload.status is not None:
            self._validate_status(payload.status)
            flight.status = payload.status.value

        return await self.flight_repository.update(flight)

    async def delete(self, flight_id: UUID) -> FlightORM | None:
        flight = await self.flight_repository.get_by_id(flight_id)
        if flight is None:
            raise FlightNotFound(
                "Рейса с id: {flight_id} не найдено."
            )

        await self.flight_repository.delete(flight)
        return flight
