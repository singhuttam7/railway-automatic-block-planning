
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Asset(Base):
    __tablename__ = "assets"

    asset_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    department_id: Mapped[str] = mapped_column(
        ForeignKey("departments.department_id"),
        nullable=False
    )

    asset_type: Mapped[str] = mapped_column(
        String(100),
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

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    criticality: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    installation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    last_maintenance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    next_maintenance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    department = relationship(
        "Department",
        back_populates="assets"
    )

    corridor = relationship(
        "Corridor",
        back_populates="assets"
    )


    maintenance_tasks = relationship(
        "MaintenanceTask",
        back_populates="asset"
    )

    defects = relationship(
        "Defect",
        back_populates="asset"
    )


