"""Tests for shipment"""

from unittest.mock import patch

import pytest
from fastapi import HTTPException

from modules.actions.shipments import get_shipment_information
from modules.database.schemas.shipment_schemas import ShipmentRequest


@patch("modules.services.weather_service.fetch_weather_condition")
def test_get_shipment_information(
    mock_fetch_weather_condition,
    create_test_db_session,
) -> None:
    """Test to get shipment informantion"""
    mock_fetch_weather_condition.return_value = {
        "description": "sunny",
        "temp": 72,
        "humidity": 50,
    }

    shipment_request = ShipmentRequest(tracking_number="TN12345678", carrier="DHL")

    shipment_response = get_shipment_information(
        create_test_db_session,
        shipment_request,
    )

    assert shipment_response.tracking_number == "TN12345678"
    assert shipment_response.sender_zip == " 10115"
    assert shipment_response.sender_country == " Germany"
    assert shipment_response.sender_city == " Berlin"
    assert shipment_response.sender_street == "Street 1"
    assert shipment_response.receiver_zip == " 75001"
    assert shipment_response.receiver_country == " France"
    assert shipment_response.receiver_city
    assert shipment_response.receiver_street
    assert shipment_response.weather


@patch("modules.services.weather_service.fetch_weather_condition")
def test_get_shipment_information_with_invalid_tracking_number(
    mock_fetch_weather_condition,
    create_test_db_session,
):
    """Test get shipment with invalid tracking number."""
    mock_fetch_weather_condition.return_value = {
        "description": "sunny",
        "temp": 72,
        "humidity": 50,
    }

    shipment_request = ShipmentRequest(tracking_number="0000", carrier="UPS")
    with pytest.raises(HTTPException) as no_shipment_found:
        get_shipment_information(create_test_db_session, shipment_request)

    assert no_shipment_found.value.status_code == 404
