from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models import Grid, Group
from .schemas import *


async def get_grids(session: AsyncSession) -> List[Grid]:
    stmt = select(Grid).order_by(Grid.id).options(selectinload(Grid.groups))
    result = await session.execute(stmt)
    grids = result.scalars().all()
    return list(grids)

async def get_grid_group(session: AsyncSession, grid_id: int) -> Grid:
    stmt = select(Grid).where(Grid.id == grid_id).order_by(Grid.id).options(selectinload(Grid.groups))
    result = await session.execute(stmt)
    grids = result.scalars().first()
    return grids

async def create_grid(session: AsyncSession, grid_in: CreateGridSchema) -> Grid:
    stmt = select(Grid).where(Grid.name == grid_in.name)
    result: Result = await session.execute(stmt)

    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Grid already exists")

    grid_data = grid_in.model_dump(exclude={'group_ids'})
    grid = Grid(**grid_data)
    session.add(grid)

    if grid_in.group_ids:
        stmt = select(Group).where(Group.id.in_(grid_in.group_ids))
        result = await session.execute(stmt)
        groups = result.scalars().all()

        # Проверяем, что все группы существуют
        found_ids = {group.id for group in groups}
        missing_ids = set(grid_in.group_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Groups not found with ids: {missing_ids}"
            )

        for group in groups:
            if group.grid_id is not None:
                raise HTTPException(
                    status_code=409,
                    detail=f"Group {group.id} is already assigned to another grid"
                )
            group.grid = grid

        await session.flush()

    await session.commit()
    await session.refresh(grid, attribute_names=['groups'])

    return grid


async def update_grid(
        session: AsyncSession,
        grid_id: int,
        grid_update: UpdateGridSchemaPartial
):
    # Явно указываем загрузку groups с помощью selectinload или joinedload
    stmt = select(Grid).where(Grid.id == grid_id).options(
        selectinload(Grid.groups)  # или joinedload(Grid.groups)
    )
    result: Result = await session.execute(stmt)
    grid = result.scalars().first()

    if not grid:
        raise HTTPException(status_code=404, detail="Grid not found")

    update_data = grid_update.model_dump(exclude_unset=True, exclude={'group_ids'})
    for field, value in update_data.items():
        setattr(grid, field, value)

    if grid_update.group_ids is not None:
        stmt = select(Group).where(Group.id.in_(grid_update.group_ids))
        result = await session.execute(stmt)
        new_groups = result.scalars().all()

        found_ids = {group.id for group in new_groups}
        missing_ids = set(grid_update.group_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Groups not found with ids: {missing_ids}"
            )

        # Проверяем, что группы не привязаны к другим гридам
        for group in new_groups:
            if group.grid_id is not None and group.grid_id != grid_id:
                raise HTTPException(
                    status_code=409,
                    detail=f"Group {group.id} is already assigned to another grid"
                )

        # Отвязываем старые группы
        for old_group in grid.groups:  # теперь groups уже загружены
            old_group.grid = None

        # Привязываем новые группы
        for new_group in new_groups:
            new_group.grid = grid

        await session.flush()

    await session.commit()

    # После коммита нужно снова обновить grid с groups
    await session.refresh(grid, attribute_names=['groups'])

    return grid