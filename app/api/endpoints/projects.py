from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_charity_before_edit,
    check_charity_exists
)
from app.core.db import get_async_session
from app.crud.project import charity_crud
from app.crud.donates import donate_crud
from app.schemas.projects import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
from app.core.user import current_superuser
from app.api.validators import check_charity_before_delete
from app.services.investition import invest_processing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],

)
async def create_charity_project(
        charity: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Создает благотворительный проект.
    """
    await check_name_duplicate(
        charity.name, session=session
    )
    new_charity = await charity_crud.create(
        obj_in=charity, session=session, apply_commit=False)
    invest_changed_list = await invest_processing(
        model_object=new_charity, session=session, crud=donate_crud
    )
    session.add_all(invest_changed_list)
    await session.commit()
    await session.refresh(new_charity)
    return new_charity


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""

    all_charity = await charity_crud.get_multi(session)
    return all_charity


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_shema: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity = await check_charity_before_edit(
        project_id, obj_shema, session=session
    )
    charity_edit = await charity_crud.update(
        db_obj=charity,
        obj_in=obj_shema,
        session=session,
    )
    return charity_edit


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства,
    его можно только закрыть.
    """
    await check_charity_exists(project_id, session)
    charity_to_delete = await charity_crud.get(project_id, session)
    check_charity_before_delete(charity_to_delete)
    charity_delete = await charity_crud.remove(charity_to_delete, session)
    return charity_delete
