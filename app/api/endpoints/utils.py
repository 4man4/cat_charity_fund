from fastapi import HTTPException, status

from app.models import CharityProject


async def get_project_or_404(project: CharityProject) -> CharityProject:
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Целевой проект не найден!',
        )
    return project
