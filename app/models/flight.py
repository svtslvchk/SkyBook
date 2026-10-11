from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.db.base import Base


class FlightORM(Base):
    __tablename__ = "flights"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    flight_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    airline_id: Mapped[UUID] = mapped_column(
        ForeignKey("airlines.id", ondelete="RESTRICT"),
        nullable=False
    )

    aircraft_id: Mapped[UUID] = mapped_column(
        ForeignKey("aircrafts.id", ondelete="RESTRICT"),
        nullable=False
    )

    origin_airport_id: Mapped[UUID] = mapped_column(
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False
    )

    destination_airport_id: Mapped[UUID] = mapped_column(
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False
    )

    departure_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    arrival_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    airline: Mapped["AirlineORM"] = relationship(
        back_populates="flights"
    )

    aircraft: Mapped["AircraftORM"] = relationship(
        back_populates="flights"
    )

    origin_airport: Mapped["AirportORM"] = relationship(
        foreign_keys=[origin_airport_id],
        back_populates="departing_flights"
    )

    destination_airport: Mapped["AirportORM"] = relationship(
        foreign_keys=[destination_airport_id],
        back_populates="arriving_flights"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('SCHEDULED', 'CANCELLED', 'DEPARTED', 'ARRIVED')",
            name="chk_flight_status",
        ),

        CheckConstraint(
            "arrival_at > departure_at",
            name="chk_flight_arrival_after_departure"
        ),

        CheckConstraint(
            "destination_airport_id <> origin_airport_id",
            name="chk_flight_different_airports"
        ),
    )
