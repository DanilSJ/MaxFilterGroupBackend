from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Grid(Base):
    name: Mapped[str] = mapped_column(String)

    # фильтры
    bad_words: Mapped[bool] = mapped_column(Boolean, default=False)
    repost: Mapped[bool] = mapped_column(Boolean, default=False)
    stop_word: Mapped[bool] = mapped_column(Boolean, default=False)
    link: Mapped[bool] = mapped_column(Boolean, default=False)
    message_delete: Mapped[bool] = mapped_column(Boolean, default=False)
    message_delete_text: Mapped[str] = mapped_column(String, default=False)

    bad_words_text: Mapped[str] = mapped_column(Text, nullable=True)
    stop_word_text: Mapped[str] = mapped_column(Text, nullable=True)

    pinned: Mapped[bool] = mapped_column(Boolean, default=False)

    groups: Mapped[list["Group"]] = relationship(
        "Group",
        back_populates="grid",
        cascade="all, delete-orphan"
    )