from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OptimizationRun(Base):
    __tablename__ = "optimization_runs"

    optimization_run_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    run_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    optimized_blocks = relationship(
        "OptimizedBlock",
        back_populates="optimization_run"
    )