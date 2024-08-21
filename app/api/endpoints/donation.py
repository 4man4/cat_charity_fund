from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.validators import (
#     check_project_exists,
#     check_reservation_intersections,
#     check_reservation_before_edit,
# )
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.crud.investments import investments_process
from app.schemas.donation import DonationCreate, DonationDB, DonationBase
from app.core.user import current_user, current_superuser
from app.models import CharityProject, User, Donation


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
    new_donation = await donation_crud.create(donation, session, user)
    await investments_process(new_donation, CharityProject, session)
    return new_donation


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
    all_donations = await donation_crud.get_multi(session)
    return all_donations


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
    donations = await donation_crud.get_donations_by_user(
        user=user, session=session
    )
    return donations
