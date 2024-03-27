from typing import Optional

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from src.schemas import (
    EventSchema, 
    BetSchema,
    EventKey,
)
from src.services import BetService, BetEventService


router = APIRouter(tags=['Bets'])


@router.get('/bets')
async def get_all_bets(service: BetService = Depends()) -> list[BetSchema]:
    return await service.get_all()


@router.post('/bets', status_code=201)
async def make_bet(
    bet: BetSchema, 
    service: BetService = Depends()
) -> BetSchema:
    return await service.create(bet)


@router.put('/event/{event_key}', description='Chages a bet status')
async def set_bet_status(
    event_key: EventKey, 
    event: EventSchema, 
    service: BetEventService = Depends()
) -> Optional[BetSchema]:
    bet = await service.set_status(event_key, **event.model_dump())
    if bet is None:
        raise HTTPException(status_code=404, detail='Event Key Does Not Exist')
    return bet
