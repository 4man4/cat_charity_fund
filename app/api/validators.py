from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import invested_amount_to_prohibit_deletion
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Целевой проект не найден!',
        )


def check_project_closed(charity_project: CharityProject) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


def check_project_invested_sum(
    charity_project: CharityProject, new_amount: int
) -> None:
    if charity_project.invested_amount > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение full_amount '
            'меньше уже вложенной суммы.',
        )


def check_project_already_invested(charity_project: CharityProject) -> None:
    if charity_project.invested_amount > invested_amount_to_prohibit_deletion:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
