from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime

from app.db.base import Base


class AirportORM(Base):
    __tablename__ = "airports"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    iata_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    departing_flights: Mapped[list["FlightORM"]] = relationship(
        foreign_keys="FlightORM.origin_airport_id",
        back_populates="origin_airport"
    )

    arriving_flights: Mapped[list["FlightORM"]] = relationship(
        foreign_keys="FlightORM.destination_airport_id",
        back_populates="destination_airport"
    )
