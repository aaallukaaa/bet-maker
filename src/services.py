from typing import Optional

from fastapi import Depends

from src.db import BetAccessObject
from src.schemas import BetSchema, EventKey, EventStatus


class BetService:
    def __init__(self, access_object: BetAccessObject = Depends()) -> None:
        self.dao = access_object
    
    async def create(self, bet: BetSchema) -> BetSchema:
        return await self.dao.save(bet)

    async def get_all(self) -> list[BetSchema]:
        return await self.dao.all()


class BetEventService:
    def __init__(self, access_object: BetAccessObject = Depends()) -> None:
        self.dao = access_object

    async def set_status(
        self, 
        event_key: EventKey, 
        status: EventStatus,
    ) -> Optional[BetSchema]:
        bet = await self.dao.by_key(event_key)
        if bet is not None:
            bet.status = status
            await self.dao.save(bet)
        return bet
