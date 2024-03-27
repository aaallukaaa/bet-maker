from pytest import mark

from src.services import BetService
from src.schemas import BetSchema

class TestBetService:
    @mark.anyio
    @mark.usefixtures('bet_db')
    @mark.parametrize(
        ('values', 'expected'),
        [
            (
                [
                    BetSchema(identity=0, bet_amount=1), 
                    BetSchema(identity=1, bet_amount=1),
                    BetSchema(identity=2, bet_amount=1),
                    BetSchema(identity=3, bet_amount=1),
                ],
                [
                    BetSchema(identity=0, bet_amount=1), 
                    BetSchema(identity=1, bet_amount=1),
                    BetSchema(identity=2, bet_amount=1),
                    BetSchema(identity=3, bet_amount=1),
                ],
            ),
            (
                [
                    BetSchema(identity='qwerty', bet_amount=1), 
                    BetSchema(identity='qwertyKey', bet_amount=1),
                    BetSchema(identity='hash', bet_amount=1),
                    BetSchema(identity='', bet_amount=1),
                ],
                [
                    BetSchema(identity='qwerty', bet_amount=1), 
                    BetSchema(identity='qwertyKey', bet_amount=1),
                    BetSchema(identity='hash', bet_amount=1),
                    BetSchema(identity='', bet_amount=1),
                ],
            ),
        ]
    )
    async def test_get_all(self, bet_db, values, expected):
        service = BetService(access_object=bet_db)
        for i in values:
            await service.create(i)
        assert await service.get_all() == expected
