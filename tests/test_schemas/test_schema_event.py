from pydantic import ValidationError
from pytest import mark, raises

from src.schemas import EventSchema


class TestEventSchema:
    @mark.parametrize(
        ('status', 'expected'),
        [
            ('LOSE', 'LOSE'),
            ('WIN', 'WIN'),
        ]
    )
    def test_valid_status(self, status, expected):
        event = EventSchema(status=status)
        assert event.status == expected

    @mark.parametrize(
        'status',
        [
            'WAIT', 'QWEFTD', 12345, '13254', [], '{"status": "WIN"}'
        ]
    )
    def test_invalid_status(self, status):
        with raises(ValidationError) as e:
            event = EventSchema(status=status)
