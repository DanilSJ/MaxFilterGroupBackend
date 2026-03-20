from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User
from .schemas import *


async def create_group(session: AsyncSession, user_in: CreateGroupSchema) -> User:
    stmt = select(User).where(User.name == user_in.name)
    result: Result = await session.execute(stmt)

    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Group already exists")

    group = User(**user_in.model_dump())
    session.add(group)
    await session.commit()
    return group

