from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations_grid_user import grid_block_users
from .base import Base


class User(Base):
    max_id: Mapped[int] = mapped_column(Integer, nullable=True)

    email: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)

    admin: Mapped[bool] = mapped_column(Boolean, default=False)

    blocked_in_grids: Mapped[list["Grid"]] = relationship(
        "Grid",
        secondary=grid_block_users,
        back_populates="block_users"
    )