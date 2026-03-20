from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import Grid
from .schemas import *


async def create_grid(session: AsyncSession, group_in: CreateGridSchema) -> Grid:
    stmt = select(Grid).where(Grid.name == group_in.name)
    result: Result = await session.execute(stmt)

    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Grid already exists")

    group = Grid(**group_in.model_dump())
    session.add(group)
    await session.commit()
    return group


async def update_grid(
        session: AsyncSession,
        grid_id: int,
        group_update: UpdateGridSchemaPartial
):
    stmt = select(Grid).where(Grid.id == grid_id)
    result: Result = await session.execute(stmt)
    group = result.scalars().first()

    if not group:
        raise HTTPException(status_code=404, detail="Grid not found")

    update_data = group_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(group, field, value)

    await session.commit()
    await session.refresh(group)

    return group