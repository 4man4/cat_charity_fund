from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    ### !!! удалить, если не используется
    async def get_project_id_by_name(
        self,
        room_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == room_name)
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

    ### !!! удалить, если не используется
    async def get_project_by_id(
        self, project_id: int, session: AsyncSession
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )
        db_project = db_project.scalars().first()
        return db_project


charity_project_crud = CRUDCharityProject(CharityProject)
