
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Department(Base):
    __tablename__ = "departments"

    department_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    department_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    assets = relationship(
        "Asset",
        back_populates="department"
    )

