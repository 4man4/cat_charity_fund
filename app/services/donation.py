from typing import Type, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import donation_crud
from app.models import Donation, User
from app.schemas import DonationBase
from app.services.base import BaseServices


class DonationServices(BaseServices):
    @classmethod
    async def create_donation(
        cls,
        obj_in: DonationBase,
        model: Type[Donation],
        session: AsyncSession = Depends(get_async_session),
        user: Optional[User] = None,
    ):
        new_object = await donation_crud.create(obj_in, session, user)
        await cls._investments_process(new_object, model, session)
        return new_object

    @staticmethod
    async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
    ):
        return await donation_crud.get_multi(session)

    @staticmethod
    async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
    ):
        return await donation_crud.get_donations_by_user(user, session)
