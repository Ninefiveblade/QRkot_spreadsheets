from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class CharityProjectBase(BaseModel):
    """ Базовая схема, extra конфигурируем исключения, если переданы
    какие-то отличные поля от схемы. """

    name: str = Field(..., max_length=100, title='Name')
    description: str = Field(..., title='Description')
    full_amount: PositiveInt = Field(..., title='Full Amount')

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    """ Схема создания проекта. """


class CharityProjectUpdate(CharityProjectCreate):
    """ Схема обновления проекта. """

    name: Optional[str] = Field(None, title='Name', max_length=100)
    description: Optional[str] = Field(None, title='Description')
    full_amount: Optional[PositiveInt] = Field(0, title='Full Amount')


class CharityProjectDB(CharityProjectBase):
    """ Схема ответа для проекта. """

    id: int
    invested_amount: int = Field(..., title='Invested Amount')
    fully_invested: bool = Field(..., title='Fully Invested')
    create_date: datetime = Field(..., title='Create Date')
    close_date: Optional[datetime] = Field(None, title='Close Date')

    class Config:
        orm_mode = True
