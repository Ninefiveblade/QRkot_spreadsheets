from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.user import User


class CRUDDonation(CRUDBase):
    """ CRUD пожертвования. """

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ):
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return donations.scalars().all()


donate_crud = CRUDDonation(Donation)
