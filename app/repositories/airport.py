from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.airport import AirportORM


class AirportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[AirportORM]:
        stmt = select(AirportORM)
        res = await self.db.scalars(stmt)
        return list(res.all())

    async def get_by_id(self, airport_id: UUID) -> AirportORM | None:
        return await self.db.get(AirportORM, airport_id)

    async def create(self, new_airport: AirportORM) -> AirportORM:
        self.db.add(new_airport)
        await self.db.commit()
        await self.db.refresh(new_airport)
        return new_airport

    async def update(self, airport_for_update: AirportORM) -> AirportORM:
        await self.db.commit()
        await self.db.refresh(airport_for_update)
        return airport_for_update

    async def delete(self, airport_for_delete: AirportORM) -> None:
        await self.db.delete(airport_for_delete)
        await self.db.commit()

    async def get_airport_by_iata_code(self, iata_code: str) -> bool:
        stmt = (
            select(AirportORM)
            .where(AirportORM.iata_code == iata_code)
            .limit(1)
        )

        found = await self.db.scalars(stmt) is not None
        return found
