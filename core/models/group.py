from sqlalchemy import String, Boolean, BigInteger, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Group(Base):
    name: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    # фильтры
    bad_words: Mapped[bool] = mapped_column(Boolean, default=False)
    repost: Mapped[bool] = mapped_column(Boolean, default=False)
    stop_word: Mapped[bool] = mapped_column(Boolean, default=False)
    link: Mapped[bool] = mapped_column(Boolean, default=False)
    message_delete: Mapped[bool] = mapped_column(Boolean, default=False)
    message_delete_text: Mapped[str] = mapped_column(String, nullable=True)

    bad_words_text: Mapped[str] = mapped_column(Text, nullable=True)
    stop_word_text: Mapped[str] = mapped_column(Text, nullable=True)

    pinned: Mapped[bool] = mapped_column(Boolean, default=False)

    grid_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("grids.id", ondelete="CASCADE"),
        nullable=True
    )

    grid: Mapped["Grid"] = relationship(
        "Grid",
        back_populates="groups"
    )
