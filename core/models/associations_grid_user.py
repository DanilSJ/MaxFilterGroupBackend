from sqlalchemy import Table, Column, ForeignKey
from .base import Base

grid_block_users = Table(
    "grid_block_users",
    Base.metadata,
    Column("grid_id", ForeignKey("grids.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)