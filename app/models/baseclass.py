from sqlalchemy import Boolean, Column, CheckConstraint, DateTime, Integer

from app.core.db import Base

BASE_MODEL_TO_REPRESENTATION = (
    "{full_amount}, "
    "{invested_amount}, "
    "{fully_invested}, "
    "{create_date}, "
    "{close_date}"
)


class BaseModel(Base):
    """ Абстрактный класс с общими полями, для
    наследования. """

    __abstract__ = True

    full_amount = Column(
        Integer,
    )
    invested_amount = Column(
        Integer,
        default=0
    )
    fully_invested = Column(
        Boolean,
        default=False
    )
    create_date = Column(
        DateTime,
    )
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    def __repr__(self) -> str:
        return BASE_MODEL_TO_REPRESENTATION.format(
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date
        )
