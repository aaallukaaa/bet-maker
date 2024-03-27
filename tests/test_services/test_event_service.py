from pytest import mark

from src.services import BetEventService
from src.schemas import BetSchema


class TestBetEventService:
    @mark.anyio
    @mark.parametrize(
        ('event_id', 'status', 'expected'),
        [
            (0, 'LOSE', BetSchema(identity=0, bet_amount=1, status='LOSE')),
            (1, 'LOSE', BetSchema(identity=1, bet_amount=1, status='LOSE')),
            (2, 'WIN', BetSchema(identity=2, bet_amount=1, status='WIN')),
            (3, 'WIN', BetSchema(identity=3, bet_amount=1, status='WIN')),
        ]
    )
    async def test_set_status(self, prepopulated_db, event_id, status, expected):
        service = BetEventService(access_object=prepopulated_db)
        res = await service.set_status(event_id, status)
        assert res == expected