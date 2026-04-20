"""create message

Revision ID: 129773955d5d
Revises: 18375837ac37
Create Date: 2026-04-20 21:41:11.169366
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '129773955d5d'
down_revision: Union[str, Sequence[str], None] = '18375837ac37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(),
            nullable=True
        )
        batch_op.alter_column(
            "password",
            existing_type=sa.VARCHAR(),
            nullable=True
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "password",
            existing_type=sa.VARCHAR(),
            nullable=False
        )
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(),
            nullable=False
        )