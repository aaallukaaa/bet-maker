from typing import Optional

from src.schemas import EventKey, BetSchema


class MockAccessObject:
    def __init__(self, prepopulated: Optional[dict] = None):
        self.storage = prepopulated or {}

    async def save(self, bet: BetSchema) -> BetSchema:
        self.storage[bet.identity] = bet
        return bet

    async def all(self) -> list[BetSchema]:
        return list(self.storage.values())

    async def by_key(self, key: EventKey) -> Optional[BetSchema]:
        return self.storage.get(key)
    
    def prepopulate(self, values: dict):
        self.storage.update(values)
