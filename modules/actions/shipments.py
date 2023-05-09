from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy.orm import Session

from modules.database.models import Carrier, Shipment
from modules.database.schemas.article_schemas import ArticleResponse
from modules.database.schemas.shipment_schemas import ShipmentRequest, ShipmentResponse
from modules.services.weather_service import fetch_weather_condition


def get_shipment_information(
    db_session: Session,
    get_shipment_info: ShipmentRequest,
) -> ShipmentResponse:
    """Get shipment information

    :param db_session: the database session
    :param get_shipment_info: the shipment information be fetched
    :return: ShipmentResponse
    """

    shipment = (
        db_session.query(Shipment)
        .join(Carrier)
        .filter(
            Shipment.tracking_number == get_shipment_info.tracking_number,
            Carrier.name == get_shipment_info.carrier,
        )
        .first()
    )

    if not shipment:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"No shipment found with payload: {str(get_shipment_info)}",
        )
    weather_data = fetch_weather_condition(
        int(shipment.receiver_zip),
        shipment.receiver_country,
    )

    return ShipmentResponse(
        tracking_number=shipment.tracking_number,
        sender_zip=shipment.sender_zip,
        sender_country=shipment.sender_country,
        sender_city=shipment.sender_city,
        sender_street=shipment.sender_street,
        receiver_zip=shipment.receiver_zip,
        receiver_country=shipment.receiver_country,
        receiver_city=shipment.receiver_city,
        receiver_street=shipment.receiver_street,
        articles=get_articles_from_shipment(shipment),
        weather=weather_data,
    )


def get_articles_from_shipment(shipment: Shipment) -> list:
    """Get articles on a particular shipment.

    :param shipment: the shipment
    :return: a list of articles
    """

    articles = []
    for aos in shipment.articles_on_shipment:
        article = aos.article
        articles.append(
            ArticleResponse(
                sku=article.sku,
                name=article.name,
                price=article.price,
                quantity=aos.quantity,
            ),
        )

    return articles
