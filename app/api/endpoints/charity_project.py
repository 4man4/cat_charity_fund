from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.api.validators import (
    check_name_duplicate,
)
from app.crud import charity_project_crud
from app.core.services import (
    investments_process,
    get_all_objects,
    partially_update_object,
    delete_object,
)
from app.models import Donation
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await investments_process(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_all_objects(charity_project_crud, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await partially_update_object(
        project_id, obj_in, charity_project_crud, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await delete_object(project_id, charity_project_crud, session)
