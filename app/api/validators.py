from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import charity_crud
from app.models import CharityProject
from app.schemas.projects import CharityProjectUpdate

DETAIL_MESSAGE_NAME_DUPLICATE = "Проект с таким именем уже существует!"
DETAIL_MESSAGE_CHARITY_EXISTS = "Проект не найден!"
DETAIL_MEDDAGE_CHECK_EDIT = "Закрытый проект нельзя редактировать!"
DETAIL_MESSAGE_ERROR_AMOUNT = "Введенная сумма меньше инвестированной."
DETAIL_MESAGE_CLOSED_PROJECT = "Нельзя удалить закрытый проект!"
DETAIL_MESAGE_PROJECT_HAVE_INVEST = "В проект были внесены средства, не подлежит удалению!"


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    name_id = await charity_crud.get_charity_by_name(name, session)
    if name_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DETAIL_MESSAGE_NAME_DUPLICATE,
        )


def check_charity_before_delete(
        project: CharityProject
) -> None:
    """ Проверка проекта перед удалением
    Недоинвестированный и закрытый удалить нельзя. """

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DETAIL_MESAGE_PROJECT_HAVE_INVEST,
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DETAIL_MESAGE_CLOSED_PROJECT,
        )


async def check_charity_exists(
        charity_id: int,
        session: AsyncSession,
) -> CharityProject:
    """ Проверка существования проекта. """

    charity = await charity_crud.get(charity_id, session)
    if charity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=DETAIL_MESSAGE_CHARITY_EXISTS
        )
    return charity


async def check_charity_before_edit(
        charity_id: int,
        obj: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    """ Проверка проекта перед удалением. """

    charity = await check_charity_exists(charity_id, session)
    if charity.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DETAIL_MEDDAGE_CHECK_EDIT
        )
    if obj.full_amount < charity.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=DETAIL_MESSAGE_ERROR_AMOUNT
        )
    if obj.name != charity.name:
        await check_name_duplicate(obj.name, session)
    return charity