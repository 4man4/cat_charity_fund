from datetime import datetime
from typing import List, Union, Tuple, Type

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import INVESTED_AMOUNT_TO_PROHIBIT_DELETION
from app.crud import charity_project_crud
from app.models import CharityProject, Donation


class BaseService:
    @staticmethod
    async def _check_name_duplicate(
        project_name: str,
        session: AsyncSession,
    ) -> None:
        project_id = await charity_project_crud.get_project_id_by_name(
            project_name, session
        )
        if project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Проект с таким именем уже существует!',
            )

    @staticmethod
    def _check_project_closed(charity_project: CharityProject) -> None:
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Закрытый проект нельзя редактировать!',
            )

    @staticmethod
    def _check_project_invested_sum(
        charity_project: CharityProject, new_amount: int
    ) -> None:
        if charity_project.invested_amount > new_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Нелья установить значение full_amount '
                'меньше уже вложенной суммы.',
            )

    @staticmethod
    def _check_project_already_invested(
        charity_project: CharityProject,
    ) -> None:
        if (
            charity_project.invested_amount >
                INVESTED_AMOUNT_TO_PROHIBIT_DELETION
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='В проект были внесены средства, не подлежит удалению!',
            )

    @staticmethod
    async def _get_uninvested_objects(
        obj_in: Type[Union[CharityProject, Donation]],
        session: AsyncSession,
    ) -> List[Union[CharityProject, Donation]]:
        objects = await session.execute(
            select(obj_in)
            .where(obj_in.fully_invested.is_(False))
            .order_by(obj_in.create_date)
        )
        return objects.scalars().all()

    @staticmethod
    def _close_object_for_donation(
        obj_in: Union[CharityProject, Donation]
    ) -> None:
        obj_in.invested_amount = obj_in.full_amount
        obj_in.fully_invested = True
        obj_in.close_date = datetime.now()

    @classmethod
    def _allocate_investment_funds(
        cls,
        obj_in: Union[CharityProject, Donation],
        model: Union[CharityProject, Donation],
    ) -> Tuple[
        Union[CharityProject, Donation], Union[CharityProject, Donation]
    ]:
        free_amount_object = obj_in.full_amount - obj_in.invested_amount
        free_amount_model = model.full_amount - model.invested_amount
        if free_amount_object > free_amount_model:
            obj_in.invested_amount += free_amount_model
            cls._close_object_for_donation(model)
        elif free_amount_object == free_amount_model:
            cls._close_object_for_donation(obj_in)
            cls._close_object_for_donation(model)
        else:
            model.invested_amount += free_amount_object
            cls._close_object_for_donation(obj_in)
        return obj_in, model

    @classmethod
    async def _investments_process(
        cls,
        obj_in: Union[CharityProject, Donation],
        model: Type[Union[CharityProject, Donation]],
        session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        objects_model = await cls._get_uninvested_objects(model, session)
        for model in objects_model:
            obj_in, model = cls._allocate_investment_funds(obj_in, model)
            session.add(obj_in)
            session.add(model)
        await session.commit()
        await session.refresh(obj_in)
        return obj_in
