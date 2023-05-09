import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy.orm import Session

from modules.actions.shipments import get_shipment_information
from modules.database.schemas.shipment_schemas import ShipmentRequest, ShipmentResponse
from modules.utilities.database import get_db_session

router = APIRouter(tags=["Shipment"])
logger = logging.getLogger(__name__)


@router.get("/shipments", response_model=ShipmentResponse)
def get_shipment(
    tracking_number: str = Query(
        ...,
        description="The tracking number of the shipment",
    ),
    carrier: str = Query(..., description="The carrier of the shipment"),
    db_session: Session = Depends(get_db_session),
) -> ShipmentResponse:
    """Get shipment and article information along with corresponding weather information."""
    try:
        logger.info("Making a request to get shipment.")
        return get_shipment_information(
            db_session,
            ShipmentRequest(tracking_number=tracking_number, carrier=carrier),
        )

    except Exception as general_exception:
        logger.error("An error occurred while trying to get shipment.")
        if general_exception.__class__.__name__ == "HTTPException":
            raise general_exception
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to get shipment information: {str(general_exception)}",
        ) from general_exception
