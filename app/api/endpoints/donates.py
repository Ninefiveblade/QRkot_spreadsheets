from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.project import charity_crud
from app.crud.donates import donate_crud
from app.schemas.donates import DonationDB, DonationAdminDB, DonationCreate
from app.core.user import current_user, current_superuser
from app.models import User
from app.schemas.user import User as UserGet
from app.services.investition import invest_processing


router = APIRouter()


@router.post('/', response_model=DonationDB, response_model_exclude_none=True)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> DonationDB:
    """Сделать пожертвование."""

    new_donation = await donate_crud.create(
        obj_in=donation,
        session=session,
        user=user,
        apply_commit=False
    )
    invest_changed_list = await invest_processing(
        model_object=new_donation, session=session, crud=charity_crud
    )
    session.add_all(invest_changed_list)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
) -> List[DonationAdminDB]:
    """
    Только для суперюзеров.
    Получает список всех пожертвований.
    """

    all_donations = await donate_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationDB],
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserGet = Depends(current_user)
) -> List[DonationDB]:
    """Получить список моих пожертвований."""
    my_donations = await donate_crud.get_by_user(session, user)
    return my_donations