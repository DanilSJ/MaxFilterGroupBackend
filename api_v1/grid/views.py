from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import schemas
from . import crud
from api_v1.auth.views import get_token, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.GridSchema)
async def create_grid(
    grid_in: schemas.CreateGridSchema,
    token: str = Depends(get_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await get_current_user(token)

    return await crud.create_grid(session=session, grid_in=grid_in)


@router.patch("/{group_id}", response_model=schemas.GridSchema)
async def update_grid(
        group_id: int,
        group_update: schemas.UpdateGridSchemaPartial,
        token: str = Depends(get_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await get_current_user(token)

    return await crud.update_grid(
        session=session,
        grid_id=group_id,
        grid_update=group_update
    )