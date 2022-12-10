from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.projects import CharityProjectDB

FORMAT = "%Y/%m/%d %H:%M:%S"
TABLE_LENGHT_FORMAT = 'A1:C{}'
VALUE_INPUT_OPTION = 'USER_ENTERED'
MAJOR_DISMENTION = 'ROWS'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """ Создает таблицу """

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:

    """ Выдает пользователю права к таблице """

    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[CharityProjectDB],
        wrapper_services: Aiogoogle
) -> None:
    """ Создает данные в таблице """

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора']
    ]
    for project in projects:
        time_different = project['close_date'] - project['create_date']
        new_row = [
            str(project['name']),
            str(time_different),
            str(project['description'])
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': MAJOR_DISMENTION,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=TABLE_LENGHT_FORMAT.format(len(table_values)),
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
