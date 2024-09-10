from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.services.donation import DonationServices
from app.schemas.donation import DonationCreate, DonationDB, DonationBase
from app.core.user import current_user, current_superuser
from app.models import CharityProject, User

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await DonationServices.create_donation(
        donation, CharityProject, session, user
    )


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await DonationServices.get_all_donations(session)


@router.get(
    '/my',
    response_model=List[DonationCreate],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех пожертвований для текущего пользователя."""
    return await DonationServices.get_user_donations(user, session)
