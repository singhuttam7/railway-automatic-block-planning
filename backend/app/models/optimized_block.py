from datetime import date, time

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OptimizedBlock(Base):
    __tablename__ = "optimized_blocks"

    optimized_block_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    corridor_id: Mapped[str] = mapped_column(
        ForeignKey("corridors.corridor_id"),
        nullable=False
    )

    block_date: Mapped[date] = mapped_column(
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

    department_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    optimization_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    corridor = relationship(
        "Corridor",
        back_populates="optimized_blocks"
    )

    block_requests = relationship(
        "BlockRequest",
        secondary="optimized_block_requests",
        back_populates="optimized_blocks"
    )