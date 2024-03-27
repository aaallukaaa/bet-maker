import json
from typing import Optional

from aioredis import from_url, Redis

from src.config import config
from src.schemas import BetSchema, EventKey


redis_url = f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}'


class RedisManager:
    def __init__(self) -> None:
        self.connection = None
    
    async def __aenter__(self) -> Redis:
        self.connection = await from_url(redis_url)
        return self.connection

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection is not None:
            await self.connection.close()
            self.connection = None


class BetAccessObject(RedisManager):
    async def save(self, bet: BetSchema) -> BetSchema:
        async with self as redis:
            key, value = bet.identity, bet.model_dump_json()
            await redis.set(key, value)
        return bet
    
    async def all(self) -> list[BetSchema]:
        async with self as redis:
            bets = []
            cursor = b"0"
            while cursor:
                cursor, keys = await redis.scan(cursor)
                values = await redis.mget(keys)
                bets.extend(BetSchema(**json.loads(i)) for i in values)
        return bets
    
    async def by_key(self, key: EventKey) -> Optional[BetSchema]:
        async with self as redis:
            value = await redis.get(key)
        return BetSchema(**json.loads(value)) if value is not None else None
