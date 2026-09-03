from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Defect(Base):
    __tablename__ = "defects"

    defect_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    asset_id: Mapped[str] = mapped_column(
        ForeignKey("assets.asset_id"),
        nullable=False
    )

    defect_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    severity_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    detected_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    target_resolution_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    estimated_repair_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    safety_risk: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    operational_impact: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    asset = relationship(
        "Asset",
        back_populates="defects"
    )