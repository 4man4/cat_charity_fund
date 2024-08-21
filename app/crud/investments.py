from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_fully_invested(
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj).where(obj.fully_invested == 0).order_by(obj.create_date)
    )
    return objects.scalars().all()


async def close_obj_for_donation(obj: Union[CharityProject, Donation]):
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


async def investing(
    obj: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    free_amount_in = obj.full_amount - obj.invested_amount
    free_amount_in_model = model.full_amount - model.invested_amount

    if free_amount_in > free_amount_in_model:
        obj.invested_amount += free_amount_in_model
        await close_obj_for_donation(model)
    elif free_amount_in == free_amount_in_model:
        await close_obj_for_donation(obj)
        await close_obj_for_donation(model)
    else:
        model.invested_amount += free_amount_in
        await close_obj_for_donation(obj)

    return obj, model


async def investments_process(
    obj: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    objects_model = await get_not_fully_invested(model, session)

    for model in objects_model:
        obj, model = await investing(obj, model)
        session.add(obj)
        session.add(model)

    await session.commit()
    await session.refresh(obj)
    return obj
