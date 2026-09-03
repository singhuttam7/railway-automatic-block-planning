
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Corridor(Base):
    __tablename__ = "corridors"

    corridor_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    corridor_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    start_km: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    end_km: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    assets = relationship(
        "Asset",
        back_populates="corridor"
    )



    trains = relationship(
        "Train",
        back_populates="corridor"
    )

    goods_forecasts = relationship(
        "GoodsForecast",
        back_populates="corridor"
    )

    block_requests = relationship(
        "BlockRequest",
        back_populates="corridor"
    )

    optimized_blocks = relationship(
        "OptimizedBlock",
        back_populates="corridor"
    )

