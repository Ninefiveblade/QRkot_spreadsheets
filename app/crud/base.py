from datetime import datetime

from typing import Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User
from app.models import CharityProject, Donation


class CRUDBase:
    """ Базовый CRUD """

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_invest_objs(
        self,
        session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(
                asc('create_date')
            )
        )
        return db_obj.scalars().all()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            create_date: bool = True,
            apply_commit: Optional[bool] = True,
    ) -> Union[CharityProject, Donation]:
        obj_with_data = obj_in.dict()
        if create_date:
            obj_with_data['create_date'] = datetime.now()
        if user is not None:
            obj_with_data['user_id'] = user.id

        db_obj = self.model(**obj_with_data, invested_amount=0)
        session.add(db_obj)
        if apply_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ) -> Union[CharityProject, Donation]:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
