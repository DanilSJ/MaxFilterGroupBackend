from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import Group
from .schemas import *

async def get_group(session: AsyncSession, group_id) -> Group | None:
    return await session.get(Group, group_id)

async def get_group_max_id(session: AsyncSession, group_id) -> Group | None:
    query = select(Group).where(Group.group_id == group_id)
    result: Result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_group(session: AsyncSession, group_in: CreateGroupSchema) -> Group:
    stmt = select(Group).where(Group.group_id == group_in.group_id)
    result: Result = await session.execute(stmt)

    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Group already exists")

    group = Group(**group_in.model_dump())
    session.add(group)
    await session.commit()
    return group


async def update_group(
        session: AsyncSession,
        group_id: int,
        group_update: UpdateGroupSchemaPartial
):
    stmt = select(Group).where(Group.id == group_id)
    result: Result = await session.execute(stmt)
    group = result.scalars().first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    update_data = group_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(group, field, value)

    await session.commit()
    await session.refresh(group)

    return group


async def delete_group(session: AsyncSession, group_id: int) -> bool:
    stmt = select(Group).where(Group.group_id == group_id)
    result: Result = await session.execute(stmt)
    group = result.scalar_one_or_none()

    if group:
        await session.delete(group)
        await session.commit()
        return True
    return False