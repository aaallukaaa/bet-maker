from decimal import Decimal

from typing import Union, Literal, Annotated

from pydantic import BaseModel, Field


BetStatus = Literal['WIN', 'LOSE', 'WAIT']

EventKey = Annotated[Union[int, str], 'EvenKey']
EventStatus = Literal['WIN', 'LOSE']


class BetSchema(BaseModel):
    identity: EventKey
    bet_amount: Annotated[Decimal, Field(allow_inf_nan=False, gt=0)]
    status: BetStatus = Field(default='WAIT')


class EventSchema(BaseModel):
    status: EventStatus
