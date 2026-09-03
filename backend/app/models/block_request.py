
from datetime import date, time

from sqlalchemy import Date, Float, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class BlockRequest(Base):
    __tablename__ = "block_requests"

    block_request_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    task_id: Mapped[str] = mapped_column(
        ForeignKey("maintenance_tasks.task_id"),
        nullable=False
    )

    corridor_id: Mapped[str] = mapped_column(
        ForeignKey("corridors.corridor_id"),
        nullable=False
    )

    location_km: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    requested_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    duration_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    task = relationship(
        "MaintenanceTask",
        back_populates="block_requests"
    )

    corridor = relationship(
        "Corridor",
        back_populates="block_requests"
    )

    optimized_blocks = relationship(
        "OptimizedBlock",
        back_populates="block_request"
    )

