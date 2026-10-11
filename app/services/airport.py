from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.airport import AirportCreateSchema, AirportUpdateSchema
from app.repositories.airport import AirportRepository
from app.models.airport import AirportORM
from app.repositories.flight import FlightRepository
from app.exceptions.airport import (
    AirportHasFlightsError, AirportNotFound
)


class AirportService:
    def __init__(self, db: AsyncSession):
        self.airport_repository = AirportRepository(db)
        self.flight_repository = FlightRepository(db)

    async def get_all(self) -> list[AirportORM]:
        return await self.airport_repository.get_all()

    async def get_by_id(self, airport_id: UUID) -> AirportORM | None:
        airport = await self.airport_repository.get_by_id(airport_id)
        if airport is None:
            raise AirportNotFound(
                "Указанный аэропорт не найден."
            )
        return airport

    async def create(self, payload: AirportCreateSchema) -> AirportORM:
        new_airport = AirportORM(
            iata_code=payload.iata_code,
            name=payload.name,
            city=payload.city,
            country=payload.country,
        )

        return await self.airport_repository.create(new_airport)

    async def update(
            self, airport_id: UUID, payload: AirportUpdateSchema
    ) -> AirportORM | None:
        airport_for_update = await self.airport_repository.get_by_id(
            airport_id)

        if airport_for_update is None:
            raise AirportNotFound(
                "Указанный аэропорт не найден."
            )

        if payload.iata_code is not None:
            airport_for_update.iata_code = payload.iata_code
        if payload.name is not None:
            airport_for_update.name = payload.name
        if payload.city is not None:
            airport_for_update.city = payload.city
        if payload.country is not None:
            airport_for_update.country = payload.country

        return await self.airport_repository.update(airport_for_update)

    async def delete(self, airport_id: UUID) -> AirportORM | None:
        airport_for_delete = await self.airport_repository.get_by_id(
            airport_id)

        has_departing_flights = (
            await self.flight_repository.exists_by_origin_airport_id(
                airport_id
            )
        )

        has_arriving_flights = (
            await self.flight_repository.exists_by_destination_airport_id(
                airport_id
            )
        )

        if has_arriving_flights or has_departing_flights:
            raise AirportHasFlightsError(
                "Нельзя удалить аэропорт, участвующий в рейсах."
            )

        if airport_for_delete is None:
            raise AirportNotFound(
                "Указанный аэропорт не найден."
            )

        await self.airport_repository.delete(airport_for_delete)
        return airport_for_delete
