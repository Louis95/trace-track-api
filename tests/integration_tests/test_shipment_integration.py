"""Shipment integration tests"""

from fastapi.testclient import TestClient

from main import app

test_client: TestClient = TestClient(app)


class TestShipmentIntegration:
    """Shipment integration tests"""

    @staticmethod
    def test_get_shipment():
        """Test get shipment with valid payload."""
        shipment_info = {"tracking_number": "TN12345678", "carrier": "DHL"}

        response = test_client.get("/shipments", params=shipment_info)

        assert response.status_code == 200
        assert response.json()["weather"]
        assert response.json()["tracking_number"]

    @staticmethod
    def test_get_shipment_with_invalid_id():
        """Test get shipment with invalid ids."""
        shipment_info = {"tracking_number": "0000000", "carrier": "UPS"}

        response = test_client.get("/shipments", params=shipment_info)

        assert response.status_code == 404
