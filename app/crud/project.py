from typing import Optional, List

from sqlalchemy import select, extract, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """ CRUD проекта. """

    async def get_charity_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(self.model).where(
                self.model.name == charity_project_name
            )
        )
        return charity_project.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        charity_project = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(True)
            ).order_by(
                asc(
                    extract('epoch', CharityProject.close_date) -
                    extract('epoch', CharityProject.create_date)
                )
            )
        )
        return charity_project.scalars().all()


charity_crud = CRUDCharityProject(CharityProject)
