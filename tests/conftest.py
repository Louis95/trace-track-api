from unittest.mock import MagicMock, patch

import pytest

from modules.database.models import Carrier, Shipment
from modules.utilities.database import SessionLocal


@pytest.fixture
def mock_search_fuzzy():
    with patch("pycountry.countries.search_fuzzy") as mock:
        yield mock


@pytest.fixture
def mock_get():
    with patch("requests.get") as mock:
        yield mock


@pytest.fixture
def mock_redis():
    with patch("redis.Redis") as mock:
        yield mock.return_value


@pytest.fixture
def db_session():
    """
    Create a new database session for each test.
    """
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_shipment(db_session):
    """
    Create a test shipment for use in the tests.
    """
    carrier = Carrier(name="DHL")
    db_session.add(carrier)
    db_session.commit()

    new_shipment = Shipment(
        tracking_number="TN12345678",
        sender_zip="10115",
        sender_country="Germany",
        sender_city="Berlin",
        sender_street="Street 10",
        receiver_zip="75001",
        receiver_country="France",
        receiver_city="Paris",
        receiver_street="Street 9",
        carrier=carrier,
    )
    shipment = (
        db_session.query(Shipment).filter_by(tracking_number="TN12345678").first()
    )
    if shipment:
        return shipment

    db_session.add(new_shipment)
    db_session.commit()

    return new_shipment
