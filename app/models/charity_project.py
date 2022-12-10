from sqlalchemy import Column, String, Text

from .baseclass import BaseModel

CHARITY_MODEL_TO_REPRESENTATION = '{name}, {description}, '


class CharityProject(BaseModel):
    """ Модель проекта """

    name = Column(
        String(100),
        unique=True,
    )
    description = Column(
        Text
    )

    def __repr__(self) -> str:
        return CHARITY_MODEL_TO_REPRESENTATION.format(
            name=self.name,
            description=self.description
        ) + super().__repr__()
