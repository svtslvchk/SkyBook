from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.db.base import Base


class AirlineORM(Base):
    __tablename__ = "airlines"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    iata_code: Mapped[str] = mapped_column(
        String(2),
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    aircrafts: Mapped[list["AircraftORM"]] = relationship(
        back_populates="airline"
    )

    flights: Mapped[list["FlightORM"]] = relationship(
        back_populates="airline"
    )
