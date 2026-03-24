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
    stmt = select(Grid).where(Grid.id == grid_id).options(
        selectinload(Grid.groups)
    )
    result: Result = await session.execute(stmt)
    grid = result.scalars().first()

    if not grid:
        raise HTTPException(status_code=404, detail="Grid not found")

    update_data = grid_update.model_dump(exclude_unset=True, exclude={'group_ids'})

    # Поля, которые нужно синхронизировать с группами
    sync_fields = {
        'bad_words', 'repost', 'stop_word', 'link',
        'message_delete', 'message_delete_text',
        'bad_words_text', 'stop_word_text',
        'message_bad_text', 'message_stop_word_text',
        'message_link_text', 'message_repost_text'
    }

    # Сохраняем старые значения для отслеживания изменений
    old_values = {}
    fields_to_sync = []

    for field, value in update_data.items():
        old_value = getattr(grid, field)
        setattr(grid, field, value)

        # Если поле из списка синхронизируемых и значение изменилось
        if field in sync_fields and old_value != value:
            fields_to_sync.append(field)
            old_values[field] = old_value

    # Обновляем текущие группы, если есть изменения в синхронизируемых полях
    if fields_to_sync and grid.groups:
        for group in grid.groups:
            for field in fields_to_sync:
                setattr(group, field, getattr(grid, field))

        # Добавляем группы в сессию для обновления
        session.add_all(grid.groups)

    # Обрабатываем обновление списка групп
    if grid_update.group_ids is not None:
        # Ищем группы по полю group_id (внешнему идентификатору)
        stmt = select(Group).where(Group.group_id.in_(grid_update.group_ids))
        result = await session.execute(stmt)
        new_groups = result.scalars().all()

        # Проверяем, что все запрошенные group_id найдены
        found_group_ids = {group.group_id for group in new_groups}
        missing_ids = set(grid_update.group_ids) - found_group_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Groups not found with group_ids: {missing_ids}"
            )

        # Проверяем, что группы не привязаны к другим сеткам
        for group in new_groups:
            if group.grid_id is not None and group.grid_id != grid_id:
                raise HTTPException(
                    status_code=409,
                    detail=f"Group with group_id {group.group_id} is already assigned to another grid"
                )

        # Отвязываем старые группы
        for old_group in grid.groups:
            old_group.grid = None

        # Привязываем новые группы и синхронизируем с ними все поля из sync_fields
        for new_group in new_groups:
            new_group.grid = grid

            # Синхронизируем все поля из sync_fields с текущими значениями grid
            for field in sync_fields:
                setattr(new_group, field, getattr(grid, field))

        session.add_all(new_groups)
        await session.flush()
    else:
        # Если group_ids не передан, но были изменения в синхронизируемых полях,
        # и при этом есть привязанные группы, они уже обновлены выше
        # Дополнительно ничего делать не нужно
        pass

    await session.commit()

    await session.refresh(grid, attribute_names=['groups'])

    return grid

async def delete_grid(session: AsyncSession, grid_id: int) -> bool:
    stmt = select(Grid).where(Grid.id == grid_id)
    result: Result = await session.execute(stmt)
    grid = result.scalar_one_or_none()

    if grid:
        await session.delete(grid)
        await session.commit()
        return True
    return False