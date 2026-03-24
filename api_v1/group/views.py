from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import schemas
from . import crud
from api_v1.auth.views import get_token, get_current_user

router = APIRouter()

@router.get("/{group_id}/", response_model=schemas.GroupSchema)
async def get_user_by_id(
    group_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    result = await crud.get_group(session, group_id)
    if not result:
        raise HTTPException(status_code=404)

    return result
@router.get("/max/{group_id}/", response_model=schemas.GroupSchema)
async def get_user_by_max_id(
    group_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    result = await crud.get_group_max_id(session, group_id)
    if not result:
        raise HTTPException(status_code=404)

    return result

@router.post("/", response_model=schemas.GroupSchema)
async def create_group(
    group_in: schemas.CreateGroupSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_group(session=session, group_in=group_in)


@router.patch("/{group_id}/", response_model=schemas.GroupSchema)
async def update_group(
        group_id: int,
        group_update: schemas.UpdateGroupSchemaPartial,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    return await crud.update_group(
        session=session,
        group_id=group_id,
        group_update=group_update
    )

@router.delete("/{group_id}/")
async def delete_group(
        group_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):

    return await crud.delete_group(
        session=session,
        group_id=group_id
    )