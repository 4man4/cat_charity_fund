from typing import Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate
from app.services.base import BaseServices


class CharityProjectServices(BaseServices):
    @classmethod
    async def create_charity_project(
        cls,
        obj_in: CharityProjectCreate,
        model: Type[CharityProject],
        session: AsyncSession = Depends(get_async_session),
    ):
        await cls._check_name_duplicate(obj_in.name, session)
        new_object = await charity_project_crud.create(obj_in, session)
        await cls._investments_process(new_object, model, session)
        return new_object

    @staticmethod
    async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await charity_project_crud.get_multi(session)

    @classmethod
    async def partially_update_charity_project(
        cls,
        obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
    ):
        await cls._check_project_exists(obj)
        cls._check_project_closed(obj)
        if obj_in.name:
            await cls._check_name_duplicate(obj_in.name, session)
        if obj_in.full_amount:
            cls._check_project_invested_sum(obj, obj_in.full_amount)
        return await charity_project_crud.update(obj, obj_in, session)

    @classmethod
    async def delete_charity_project(
        cls,
        obj_id: int,
        session: AsyncSession = Depends(get_async_session),
    ):
        obj = await charity_project_crud.get(obj_id=obj_id, session=session)
        await cls._check_project_exists(obj)
        cls._check_project_already_invested(obj)
        return await charity_project_crud.remove(db_obj=obj, session=session)
