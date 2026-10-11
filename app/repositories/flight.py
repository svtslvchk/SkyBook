from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.flight import FlightORM


class FlightRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[FlightORM]:
        res = await self.db.scalars(select(FlightORM))
        return list(res.all())

    async def get_by_id(self, flight_id: UUID) -> FlightORM | None:
        flight = await self.db.get(FlightORM, flight_id)
        return flight

    async def create(self, new_flight: FlightORM) -> FlightORM:
        self.db.add(new_flight)
        await self.db.commit()
        await self.db.refresh(new_flight)
        return new_flight

    async def update(self, flight_for_update: FlightORM) -> FlightORM:
        await self.db.commit()
        await self.db.refresh(flight_for_update)
        return flight_for_update

    async def delete(self, flight_for_delete: FlightORM) -> None:
        await self.db.delete(flight_for_delete)
        await self.db.commit()

    async def exists_by_airline_id(self, airline_id: UUID) -> bool:
        stmt = (
            select(FlightORM)
            .where(FlightORM.airline_id == airline_id)
            .limit(1)
        )
        res = await self.db.scalars(stmt)
        return res is not None

    async def exists_by_aircraft_id(self, aircraft_id: UUID) -> bool:
        stmt = (
            select(FlightORM)
            .where(FlightORM.aircraft_id == aircraft_id)
            .limit(1)
        )
        res = await self.db.scalars(stmt)
        return res is not None

    async def exists_by_origin_airport_id(
            self, origin_airport_id: UUID
    ) -> bool:
        stmt = (
            select(FlightORM)
            .where(FlightORM.origin_airport_id == origin_airport_id)
            .limit(1)
        )

        res = await self.db.scalars(stmt)
        return res is not None

    async def exists_by_destination_airport_id(
            self, destination_airport_id: UUID
    ) -> bool:
        stmt = (
            select(FlightORM)
            .where(FlightORM.destination_airport_id == destination_airport_id)
            .limit(1)
        )

        res = await self.db.scalars(stmt)
        return res is not None
