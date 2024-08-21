from datetime import datetime
from typing import List, Union, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_uninvested_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj_in).where(obj_in.fully_invested == 0)
        .order_by(obj_in.create_date)
    )
    return objects.scalars().all()


async def close_object_for_donation(
        obj_in: Union[CharityProject, Donation]
) -> None:
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()


async def allocate_investment_funds(
    obj_in: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
) -> Tuple[Union[CharityProject, Donation], Union[CharityProject, Donation]]:
    free_amount_object = obj_in.full_amount - obj_in.invested_amount
    free_amount_model = model.full_amount - model.invested_amount

    if free_amount_object > free_amount_model:
        obj_in.invested_amount += free_amount_model
        await close_object_for_donation(model)
    elif free_amount_object == free_amount_model:
        await close_object_for_donation(obj_in)
        await close_object_for_donation(model)
    else:
        model.invested_amount += free_amount_object
        await close_object_for_donation(obj_in)

    return obj_in, model


async def investments_process(
    obj_in: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    objects_model = await get_uninvested_objects(model, session)

    for model in objects_model:
        obj_in, model = await allocate_investment_funds(obj_in, model)
        session.add(obj_in)
        session.add(model)

    await session.commit()
    await session.refresh(obj_in)
    return obj_in
