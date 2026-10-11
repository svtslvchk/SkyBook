from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.repositories.airline import AirlineRepository
from app.models.airline import AirlineORM
from app.schemas.airline import (
    AirlineCreateSchema,
    AirlineUpdateSchema
)
from app.exceptions.airline import (
    AirlineHasAircraftError,
    NonUniqueIataCode, AirlineNotFound
)
from app.repositories.aircraft import AircraftRepository
from app.repositories.flight import FlightRepository
from app.exceptions.airline import AirlineHasFlightError


class AirlineService:
    def __init__(self, db: AsyncSession):
        self.airline_repository = AirlineRepository(db)
        self.aircraft_repository = AircraftRepository(db)
        self.flight_repository = FlightRepository(db)

    async def get_all(self) -> list[AirlineORM]:
        return await self.airline_repository.get_all()

    async def get_by_id(self, airline_id: UUID) -> AirlineORM | None:
        target_airline = await self.airline_repository.get_by_id(airline_id)
        if target_airline is None:
            raise AirlineNotFound(
                "Указанная авиакомпания не найдена."
            )
        return target_airline

    async def create(self, payload: AirlineCreateSchema) -> AirlineORM:
        chk_un_iata_code = await self.airline_repository.get_airport_by_iata_code(
            payload.iata_code
        )
        if chk_un_iata_code:
            raise NonUniqueIataCode(
                f"iata_code: {payload.iata_code} " +
                "уже существует."
            )
        new_airline = AirlineORM(
            name=payload.name,
            iata_code=payload.iata_code
        )

        return await self.airline_repository.create(new_airline)

    async def update(
            self, airline_id: UUID, payload: AirlineUpdateSchema
    ) -> AirlineORM | None:
        airline_for_update = await self.airline_repository.get_by_id(
            airline_id
        )
        if airline_for_update is None:
            raise AirlineNotFound(
                "Указанная авиакомпания не найдена."
            )

        if payload.name is not None:
            airline_for_update.name = payload.name
        if payload.iata_code is not None:
            airline_for_update.iata_code = payload.iata_code

        return await self.airline_repository.update(airline_for_update)

    async def delete(self, airline_id: UUID) -> AirlineORM | None:
        airline_for_delete = await self.airline_repository.get_by_id(
            airline_id
        )
        if airline_for_delete is None:
            raise AirlineNotFound(
                "Указанная авиакомпания не найдена."
            )
        has_aircrafts = await self.aircraft_repository.exists_by_airline_id(
            airline_id
        )
        if has_aircrafts:
            raise AirlineHasAircraftError(
                "Нельзя удалить авиакомпанию, у которой есть самолеты."
            )

        has_flights = (
            await self.flight_repository.exists_by_airline_id(
                airline_id
            )
        )

        if has_flights:
            raise AirlineHasFlightError(
                "Нельзя удалить авиакомпанию, у которой есть рейсы."
            )

        await self.airline_repository.delete(airline_for_delete)
        return airline_for_delete
