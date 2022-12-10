from datetime import datetime
from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.crud import donates, project


async def invest_processing(
    model_object: Union[Donation, CharityProject],
    crud: Union[donates.Donation, project.CharityProject],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    '''Процесс распределения инвестиций.'''

    crud_objects = await crud.get_invest_objs(session)
    invest_changed_list = []
    for crud_object in crud_objects:
        total_invest_distribution = min(
            model_object.full_amount - model_object.invested_amount,
            crud_object.full_amount - crud_object.invested_amount
        )
        for iter_obj in (crud_object, model_object):
            if total_invest_distribution == 0:
                break
            iter_obj.invested_amount += total_invest_distribution
            if iter_obj.full_amount == iter_obj.invested_amount:
                iter_obj.fully_invested = True
                iter_obj.close_date = datetime.now()
                invest_changed_list.append(iter_obj)
    return invest_changed_list
