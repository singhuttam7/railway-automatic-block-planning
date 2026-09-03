
from datetime import date

from sqlalchemy import Date, Integer, String, ForeignKey
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

    severity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    reported_date: Mapped[date] = mapped_column(
        Date,
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

