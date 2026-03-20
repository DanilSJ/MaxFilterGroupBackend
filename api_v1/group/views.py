from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import schemas
from . import crud
from api_v1.auth.views import get_token, get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.GroupSchema)
async def create_group(
    group_in: schemas.CreateGroupSchema,
    token: str = Depends(get_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await get_current_user(token)

    return await crud.create_group(session=session, user_in=group_in)
