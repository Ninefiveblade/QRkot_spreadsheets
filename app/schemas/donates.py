from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    """ Базовая схема проекта. """

    full_amount: PositiveInt = Field(..., title="Full Amount")
    comment: Optional[str] = None

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """ Схема создания проекта. """


class DonationDB(DonationBase):
    """ Схема ответа для проекта. (для юзера) """

    id: int
    create_date: datetime = Field(..., title='Create Date')

    class Config:
        orm_mode = True


class DonationAdminDB(DonationDB):
    """ Схема ответа для проекта. (для суперюзера) """

    user_id: int = Field(..., title='User Id')
    invested_amount: int = Field(..., title='Invested Amount')
    fully_invested: bool = Field(..., title='Fully Invested')
    close_date: Optional[datetime] = Field(None, title='Close Date')

    class Config:
        orm_mode = True
