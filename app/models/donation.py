from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Text
)

from .baseclass import BaseModel


DONATION_MODEL_TO_REPRESENTATION = '{user_id}, {comment}, '


class Donation(BaseModel):

    user_id = Column(String, ForeignKey(
        'user.id',
    ))
    comment = Column(Text)

    def __repr__(self) -> str:
        return DONATION_MODEL_TO_REPRESENTATION.format(
            user_id=self.user_id,
            comment=self.comment
        ) + super().__repr__()
