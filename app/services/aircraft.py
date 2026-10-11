from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.aircraft import AircraftORM
from app.schemas.aircraft import AircraftCreateSchema, AircraftUpdateSchema
from app.repositories.aircraft import AircraftRepository
from app.repositories.airline import AirlineRepository
from app.exceptions.aircraft import (
    NonExsistentAirline, AircraftHasFlightsError,
    AircraftNotFound
)
from app.repositories.flight import FlightRepository


class AircraftService:
    def __init__(self, db: AsyncSession):
        self.aircraft_repository = AircraftRepository(db)
        self.airline_repository = AirlineRepository(db)
        self.flight_repository = FlightRepository(db)

    async def get_all(self) -> list[AircraftORM]:
        return await self.aircraft_repository.get_all()

    async def get_by_id(self, aircraft_id: UUID) -> AircraftORM:
        aircraft = await self.aircraft_repository.get_by_id(
            aircraft_id
        )

        if aircraft is None:
            raise AircraftNotFound(
                "Указанный самолет не найден."
            )

        return aircraft

    async def create(self, payload: AircraftCreateSchema
                     ) -> AircraftORM:
        airline = await self.airline_repository.get_by_id(payload.airline_id)
        if airline is None:
            raise NonExsistentAirline(
                "Самолет не может принадлежать несуществующей авиакомпании."
            )

        new_aircraft = AircraftORM(
            airline_id=payload.airline_id,
            model=payload.model,
            registration_number=payload.registration_number,
            seat_capacity=payload.seat_capacity
        )

        return await self.aircraft_repository.create(new_aircraft)

    async def update(
            self, aircraft_id: UUID, payload: AircraftUpdateSchema
    ) -> AircraftORM | None:
        aircraft = await self.aircraft_repository.get_by_id(aircraft_id)
        if aircraft is None:
            raise AircraftNotFound(
                "Указанный самолет не найден."
            )

        if payload.airline_id is not None:
            airline = await self.airline_repository.get_by_id(
                payload.airline_id)

            if airline is None:
                raise NonExsistentAirline(
                    "Самолет не может пр надлежать несуществующей авиакомпании"
                )

            aircraft.airline_id = payload.airline_id

        if payload.model is not None:
            aircraft.model = payload.model

        if payload.seat_capacity is not None:
            aircraft.seat_capacity = payload.seat_capacity

        if payload.registration_number is not None:
            aircraft.registration_number = payload.registration_number

        return await self.aircraft_repository.update(aircraft)

    async def delete(self, aircraft_id: UUID) -> AircraftORM | None:
        aircraft = await self.aircraft_repository.get_by_id(aircraft_id)
        if aircraft is None:
            raise AircraftNotFound(
                "Указанный самолет не найден."
            )

        has_flights = (
            await self.flight_repository.exists_by_aircraft_id(
                aircraft_id
            )
        )

        if has_flights:
            raise AircraftHasFlightsError(
                "Нельзя удалить самолет, участвующий в полетах."
            )
        await self.aircraft_repository.delete(aircraft)
        return aircraft
