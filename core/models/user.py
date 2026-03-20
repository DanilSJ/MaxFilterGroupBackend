from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    admin: Mapped[bool] = mapped_column(Boolean, default=False)