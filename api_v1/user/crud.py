from fastapi import HTTPException
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User
from .schemas import *
import bcrypt


async def create_user(session: AsyncSession, user_in: RegisterSchema) -> User:
    stmt = select(User).where(User.email == user_in.email)
    result: Result = await session.execute(stmt)

    if result.scalars().first():
        raise HTTPException(status_code=409, detail="User already exists")

    if not user_in.password:
        user_in.password = ""

    hashed = bcrypt.hashpw(user_in.password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    user_in.password = hashed

    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def login_user(session: AsyncSession, email: str, password: str) -> User:
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.password:
        raise HTTPException(status_code=400, detail="Password not set")

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user