
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    task_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    asset_id: Mapped[str] = mapped_column(
        ForeignKey("assets.asset_id"),
        nullable=False
    )

    task_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    priority: Mapped[int] = mapped_column(
    Integer,
    nullable=False
)

    priority_score: Mapped[float | None] = mapped_column(
    Float,
    nullable=True
)

    priority_level: Mapped[str | None] = mapped_column(
    String(20),
    nullable=True
)

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    estimated_duration_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    asset = relationship(
        "Asset",
        back_populates="maintenance_tasks"
    )

    block_requests = relationship(
        "BlockRequest",
        back_populates="task"
    )

