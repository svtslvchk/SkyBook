from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.airline import AirlineORM


class AirlineRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[AirlineORM]:
        res = await self.db.scalars(
            select(AirlineORM)
        )
        return list(res)

    async def get_by_id(self, airline_id: UUID) -> AirlineORM | None:
        return await self.db.get(AirlineORM, airline_id)

    async def create(self, new_airline: AirlineORM) -> AirlineORM:
        self.db.add(new_airline)
        await self.db.commit()
        await self.db.refresh(new_airline)
        return new_airline

    async def update(self, airline_for_update: AirlineORM) -> AirlineORM:
        await self.db.commit()
        await self.db.refresh(airline_for_update)
        return airline_for_update

    async def delete(self, airline_for_delete: AirlineORM) -> None:
        await self.db.delete(airline_for_delete)
        await self.db.commit()

    async def get_airport_by_iata_code(self, iata_code: str) -> bool:
        stmt = (
            select(AirlineORM)
            .where(AirlineORM.iata_code == iata_code)
            .limit(1)
        )

        found = await self.db.scalars(stmt) is not None
        return found
