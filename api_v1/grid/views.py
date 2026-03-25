from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import schemas
from . import crud
from api_v1.auth.views import get_token, get_current_user

router = APIRouter()


@router.get("s/", response_model=List[schemas.GridSchema])
async def grids(
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await crud.get_grids(session=session)

@router.post("/", response_model=schemas.GridSchema)
async def create_grid(
    grid_in: schemas.CreateGridSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_grid(session=session, grid_in=grid_in)

@router.get("/{grid_id}/", response_model=schemas.GridSchema)
async def get_grid_group(
    grid_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await crud.get_grid_group(session=session, grid_id=grid_id)


@router.patch("/{grid_id}/", response_model=schemas.GridSchema)
async def update_grid(
        grid_id: int,
        group_update: schemas.UpdateGridSchemaPartial,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await crud.update_grid(
        session=session,
        grid_id=grid_id,
        grid_update=group_update
    )

@router.delete("/{grid_id}/")
async def delete_grid(
        grid_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):

    return await crud.delete_grid(
        session=session,
        grid_id=grid_id
    )