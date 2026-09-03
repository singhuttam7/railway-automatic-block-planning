
from datetime import date, time

from sqlalchemy import Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Train(Base):
    __tablename__ = "trains"

    train_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    corridor_id: Mapped[str] = mapped_column(
        ForeignKey("corridors.corridor_id"),
        nullable=False
    )

    train_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    train_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    date: Mapped[date] = mapped_column(
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

    corridor = relationship(
        "Corridor",
        back_populates="trains"
    )

