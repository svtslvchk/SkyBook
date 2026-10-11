from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.aircraft import AircraftORM


class AircraftRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[AircraftORM]:
        res = await self.db.scalars(select(AircraftORM))
        return list(res)

    async def get_by_id(self, aircraft_id: UUID) -> AircraftORM | None:
        target_aircraft = await self.db.get(AircraftORM, aircraft_id)
        return target_aircraft

    async def create(self, new_aircraft: AircraftORM) -> AircraftORM:
        self.db.add(new_aircraft)
        await self.db.commit()
        await self.db.refresh(new_aircraft)
        return new_aircraft

    async def update(self, aircraft_for_update: AircraftORM) -> AircraftORM:
        await self.db.commit()
        await self.db.refresh(aircraft_for_update)
        return aircraft_for_update

    async def delete(self, aircraft_for_delete: AircraftORM) -> None:
        await self.db.delete(aircraft_for_delete)
        await self.db.commit()

    async def exists_by_airline_id(self, airline_id: UUID) -> bool:
        stmt = (
            select(AircraftORM.id)
            .where(AircraftORM.airline_id == airline_id)
            .limit(1)
        )

        res = await self.db.scalars(stmt)
        return res is not None
