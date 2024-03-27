from pytest import mark

from httpx import AsyncClient, ASGITransport

from src.main import app
from src.schemas import BetSchema


BASE_URL = "http://localhost:8000"



@mark.anyio
@mark.parametrize(
    ('request_values', 'valid_values'),
    [
        (
            {"identity": 1, "bet_amount": 1.0, "status": "WAIT"},
            {"identity": 1, "bet_amount": 1.0, "status": "WAIT"}
        ),
        (
            {"identity": 2, "bet_amount": 23.20, "status": "WAIT"},
            {"identity": 2, "bet_amount": 23.20, "status": "WAIT"}
        ),
        (
            {"identity": "KEY", "bet_amount": 84.99, "status": "WAIT"},
            {"identity": "KEY", "bet_amount": 84.99, "status": "WAIT"}
        ),
        (
            {"identity": 784, "bet_amount": 0.1, "status": "WAIT"},
            {"identity": 784, "bet_amount": 0.1, "status": "WAIT"}
        ),
        (
            {"identity": 2, "bet_amount": 23.20},
            {"identity": 2, "bet_amount": 23.20, "status": "WAIT"}
        )
    ]
)
async def test_create_201(mock_db, request_values, valid_values):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post('/bets', json=request_values)
    expected_model = BetSchema.model_validate(valid_values)
    response_model = BetSchema.model_validate(response.json())
    assert response.status_code == 201
    assert expected_model == response_model


@mark.anyio
@mark.parametrize(
    'request_values',
    [
        {},
        {"status": "WAIT"},
        {"identity": 2, "status": "WAIT"},
        {"bet_amount": 23.20, "status": "WAIT"},
        {"identity": 1, "bet_amount": 0, "status": "WAIT"},
        {"identity": 1, "bet_amount": -1, "status": "WAIT"},
        {"identity": 1, "bet_amount": 1, "status": "INVALID STATUS"},
    ]
)
async def test_create_422(mock_db, request_values):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post('/bets', json=request_values)
    assert response.status_code == 422
