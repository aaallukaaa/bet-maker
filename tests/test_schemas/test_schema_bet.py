from decimal import Decimal

from pydantic import ValidationError
from pytest import mark, raises

from src.schemas import BetSchema


class TestBetSchemaIdentity:
    @mark.parametrize(
        ('identity', 'expected'),
        [
            (0, 0),
            (1, 1),
            (-1, -1),
            ('', ''),
            ('qwerty', 'qwerty'),
            ('qazxswedc', 'qazxswedc'),
            ("{value: 123}", "{value: 123}"),
        ]
    )
    def test_valid_identity(self, identity, expected):
        bet = BetSchema(identity=identity, bet_amount=1)
        assert bet.identity == expected


class TestBetSchemaAmount:
    @mark.parametrize(
        'bet_amount',
        [
            'abcd',
            '0',
            0,
            -1,
            '-1',
            '-9999',
            -9999,
            '/123/'
        ]
    )
    def test_invalid_amount(self, bet_amount):
        with raises(ValidationError):
            bet = BetSchema(identity=1, bet_amount=bet_amount)

    @mark.parametrize(
        ('bet_amount', 'expected'),
        [
            ('0.99', Decimal('0.99')),
            ('0.0000000000000001', Decimal('0.0000000000000001')),
            (1, Decimal('1.00'),),
            (1245, Decimal('1245.00'),),
            (99, Decimal('99.00'),),
            (1, Decimal('1.00'),),
        ]
    )
    def test_valid_amount(self, bet_amount, expected):
        bet = BetSchema(identity=1, bet_amount=bet_amount)
        assert isinstance(bet.bet_amount, Decimal)
        assert bet.bet_amount == expected


class TestBetSchemaStatus:
    @mark.parametrize(
        ("identity", "bet_amount"), 
        [
            (0, 1.00),
            (1, 2.00),
            (2, 200),
            (3, 999.999),
            (4, "100.28"),
        ]
    )
    def test_default_status(self, identity, bet_amount):
        bet = BetSchema(identity=identity, bet_amount=bet_amount)
        assert bet.status == 'WAIT'
    
    @mark.parametrize(
        'status',
        [
            '',
            'QWERTY',
            'WAITPLS',
            'CONTINUING',
            123456789,
            789,
        ]
    )
    def test_invalid_status(self, status):
        with raises(ValidationError) as e:
            bet = BetSchema(identity=1, bet_amount=1.0, status=status)
    
    @mark.parametrize(
        ('status', 'expected'),
        [
            ('WAIT', 'WAIT'),
            ('WIN', 'WIN'),
            ('LOSE', 'LOSE'),
        ]
    )
    def test_set_status(self, status, expected):
        bet = BetSchema(identity=1, bet_amount=1.0, status=status)
        assert bet.status == expected
