from pytest import fixture

from src.main import app
from src.schemas import BetSchema
from src.db import BetAccessObject

from .mock_services import MockAccessObject


@fixture
def bet_db():
    return MockAccessObject()


@fixture
def prepopulated_db():
    m = MockAccessObject()
    m.prepopulate({i: BetSchema(identity=i, bet_amount=1) for i in range(10)})
    return m


@fixture
def mock_db():
    app.dependency_overrides[BetAccessObject] = MockAccessObject
