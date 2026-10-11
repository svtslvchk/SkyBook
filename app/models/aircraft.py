from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.db.base import Base


class AircraftORM(Base):
    __tablename__ = "aircrafts"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    airline_id: Mapped[UUID] = mapped_column(
        ForeignKey("airlines.id", ondelete="RESTRICT"),
        nullable=False
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    registration_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    seat_capacity: Mapped[int] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    airline: Mapped["AirlineORM"] = relationship(
        back_populates="aircrafts"
    )

    flights: Mapped[list["FlightORM"]] = relationship(
        back_populates="aircraft"
    )

    __table_args__ = (
        CheckConstraint(
            "seat_capacity > 0",
            name="chk_airport_capacity"
        ),
    )
