from datetime import datetime
from typing import List, Union, Tuple, Type, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_project_closed,
    check_project_invested_sum,
    check_project_already_invested,
)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import CRUDBase, charity_project_crud
from app.crud.donation import CRUDDonation
from app.models import CharityProject, Donation, User
from app.schemas import (
    CharityProjectCreate,
    DonationBase,
    CharityProjectUpdate,
)


async def get_uninvested_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj_in)
        .where(obj_in.fully_invested.is_(False))
        .order_by(obj_in.create_date)
    )
    return objects.scalars().all()


def close_object_for_donation(obj_in: Union[CharityProject, Donation]) -> None:
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()


def allocate_investment_funds(
    obj_in: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
) -> Tuple[Union[CharityProject, Donation], Union[CharityProject, Donation]]:
    free_amount_object = obj_in.full_amount - obj_in.invested_amount
    free_amount_model = model.full_amount - model.invested_amount
    if free_amount_object > free_amount_model:
        obj_in.invested_amount += free_amount_model
        close_object_for_donation(model)
    elif free_amount_object == free_amount_model:
        close_object_for_donation(obj_in)
        close_object_for_donation(model)
    else:
        model.invested_amount += free_amount_object
        close_object_for_donation(obj_in)
    return obj_in, model


async def investments_process(
    obj_in: Union[CharityProject, Donation],
    model: Type[Union[CharityProject, Donation]],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    objects_model = await get_uninvested_objects(model, session)

    for model in objects_model:
        obj_in, model = allocate_investment_funds(obj_in, model)
        session.add(obj_in)
        session.add(model)

    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def create_object(
    obj_in: Union[CharityProjectCreate, DonationBase],
    crud_class: Type[CRUDBase],
    model: Type[Union[CharityProject, Donation]],
    session: AsyncSession = Depends(get_async_session),
    user: Optional[User] = None,
):
    if crud_class == charity_project_crud:
        await check_name_duplicate(obj_in.name, session)
    new_object = await crud_class.create(
        obj_in=obj_in, session=session, user=user
    )
    await investments_process(new_object, model, session)
    return new_object


async def get_all_objects(
    crud_class: Type[CRUDBase],
    session: AsyncSession = Depends(get_async_session),
):
    return await crud_class.get_multi(session)


async def partially_update_object(
    obj_id: int,
    obj_in: CharityProjectUpdate,
    crud_class: Type[CRUDBase],
    session: AsyncSession = Depends(get_async_session),
):
    await check_project_exists(obj_id, session)
    object = await crud_class.get(obj_id=obj_id, session=session)
    check_project_closed(object)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        check_project_invested_sum(object, obj_in.full_amount)
    return await crud_class.update(object, obj_in, session)


async def delete_object(
    obj_id: int,
    crud_class: Type[CRUDBase],
    session: AsyncSession = Depends(get_async_session),
):
    await check_project_exists(obj_id, session)
    object = await crud_class.get(obj_id=obj_id, session=session)
    check_project_already_invested(object)
    return await crud_class.remove(db_obj=object, session=session)


async def get_user_objects(
    crud_class: Type[CRUDDonation],
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud_class.get_donations_by_user(user, session)
