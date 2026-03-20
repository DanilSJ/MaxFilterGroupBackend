from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper
from . import schemas
from . import crud
from api_v1.auth.views import (
    create_access_token,
    get_current_user,
    get_token,
    Token,
)
from core.config import auth_settings

router = APIRouter()


@router.post("/", response_model=schemas.UserSchema)
async def create_user(
    user_in: schemas.RegisterSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.post("/login/")
async def login_user(
    data: schemas.LoginSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.login_user(session, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/auth/check/")
async def auth_check(token: str = Depends(get_token)):
    return await get_current_user(token)