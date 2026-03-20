from sqlalchemy import String, Boolean, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Group(Base):
    name: Mapped[str] = mapped_column(String)

    # фильтры
    bad_words: Mapped[bool] = mapped_column(Boolean, default=False)
    repost: Mapped[bool] = mapped_column(Boolean, default=False)
    stop_word: Mapped[bool] = mapped_column(Boolean, default=False)
    link: Mapped[bool] = mapped_column(Boolean, default=False)
    message_delete: Mapped[bool] = mapped_column(Boolean, default=False)

    bad_words_text: Mapped[str] = mapped_column(Text, nullable=True)
    stop_word_text: Mapped[str] = mapped_column(Text, nullable=True)

    pinned: Mapped[bool] = mapped_column(Boolean, default=False)