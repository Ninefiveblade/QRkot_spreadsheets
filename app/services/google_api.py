from datetime import datetime
from typing import List
import copy

from aiogoogle.excs import ValidationError
from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.projects import CharityProjectDB

FORMAT = '%Y/%m/%d %H:%M:%S'
TABLE_LENGHT_FORMAT = 'A1:C{}'
VALUE_INPUT_OPTION = 'USER_ENTERED'
MAJOR_DISMENTION = 'ROWS'
TITLE_SPREADSHEET = 'Отчет от {}'
TABLE_VALUES = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора']
]
TABLE_MAX_ROWS = 100
TABLE_MAX_COLUMNS = 11
CREATE_TABLE_ERROR = (
    "Недопустимое количество создаваемых ячеек\n"
    "Максимальное количество строк: {TABLE_MAX_ROWS}\n"
    "Максимальное количество колонок: {TABLE_MAX_COLUMNS}\n"
    "Введенное количество строк: {current_rows}\n"
    "Введенное количество колонок: {current_columns}\n"
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """ Создает таблицу """

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    datetime_title = TITLE_SPREADSHEET.format(now_date_time)
    spreadsheet_body = dict(
        properties=dict(
            title=datetime_title,
            locale='ru_RU',
        ),
        sheets=[dict(properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=TABLE_MAX_ROWS,
                columnCount=TABLE_MAX_COLUMNS,
            )
        ))]
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:

    """ Выдает пользователю права к таблице """

    permissions_body = dict(
        type='user',
        role='writer',
        emailAddress=settings.email
    )
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List[CharityProjectDB],
        wrapper_services: Aiogoogle
) -> None:
    """ Создает данные в таблице """

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = copy.deepcopy(TABLE_VALUES)
    table_head[0][1] = now_date_time
    table_values = [
        *table_head,
        *[list(map(str, field)) for field in projects],
    ]
    current_row, current_column = (len(table_values), max(len(value) for value in table_head))
    if current_row > TABLE_MAX_ROWS or current_column > TABLE_MAX_COLUMNS:
        raise ValidationError(
            CREATE_TABLE_ERROR.format(
                TABLE_MAX_ROWS=TABLE_MAX_ROWS,
                TABLE_MAX_COLUMNS=TABLE_MAX_COLUMNS,
                current_column=current_column,
                current_row=current_row),
        )
    update_body = dict(
        majorDimension=MAJOR_DISMENTION,
        values=table_values
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{TABLE_MAX_ROWS}C{TABLE_MAX_COLUMNS}',
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
