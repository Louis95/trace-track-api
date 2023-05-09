"""Conftest file"""

from unittest.mock import patch

import pytest

from modules.database.models import Carrier, Shipment
from modules.utilities.database import SessionLocal


@pytest.fixture
def mock_search_fuzzy():
    """Mock search_fuzzy function"""
    with patch("pycountry.countries.search_fuzzy") as mock:
        yield mock


@pytest.fixture
def mock_get():
    """Mock for get request"""
    with patch("requests.get") as mock:
        yield mock


@pytest.fixture
def mock_redis():
    """Redis mock"""
    with patch("redis.Redis") as mock:
        yield mock.return_value


@pytest.fixture
def create_test_db_session():
    """
    Create a new database session for each test.
    """
    test_db = SessionLocal()
    yield test_db
    test_db.close()


@pytest.fixture
def create_test_shipment():
    """
    Create a test shipment for use in the tests.
    """
    carrier = Carrier(name="DHL")
    create_test_db_session.add(carrier)
    create_test_db_session.commit()

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
        create_test_db_session.query(Shipment)
        .filter_by(tracking_number="TN12345678")
        .first()
    )
    if shipment:
        return shipment

    create_test_db_session.add(new_shipment)
    create_test_db_session.commit()

    return new_shipment
