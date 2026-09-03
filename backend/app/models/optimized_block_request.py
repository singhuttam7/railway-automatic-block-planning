from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class OptimizedBlockRequest(Base):
    __tablename__ = "optimized_block_requests"

    optimized_block_id: Mapped[str] = mapped_column(
        ForeignKey("optimized_blocks.optimized_block_id"),
        primary_key=True
    )

    block_request_id: Mapped[str] = mapped_column(
        ForeignKey("block_requests.block_request_id"),
        primary_key=True
    )