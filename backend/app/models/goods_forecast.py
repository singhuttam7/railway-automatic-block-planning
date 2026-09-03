
from datetime import date, time

from sqlalchemy import Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class GoodsForecast(Base):
    __tablename__ = "goods_forecasts"

    forecast_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    corridor_id: Mapped[str] = mapped_column(
        ForeignKey("corridors.corridor_id"),
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

    expected_goods_trains: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    corridor = relationship(
        "Corridor",
        back_populates="goods_forecasts"
    )

