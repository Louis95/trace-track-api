"""Models defining the Shipment related tables"""

from typing import List

from pydantic import BaseModel, Field

from modules.database.schemas.article_schemas import ArticleResponse


class ShipmentRequest(BaseModel):
    """Shipment model"""

    tracking_number: str = Field(..., description="The tracking number of the shipment")
    carrier: str = Field(..., description="The carrier of the shipment")


class ShipmentResponse(BaseModel):
    """Shipment Response model"""

    tracking_number: str = Field(None, description="Tracking number")
    sender_zip: str = Field(None, description="Sender's zip code")
    sender_country: str = Field(None, description="Sender country")
    sender_city: str = Field(None, description="Sender city")
    sender_street: str = Field(None, description="Sender Street")
    receiver_zip: str = Field(None, description="Receiver zip code")
    receiver_country: str = Field(None, description="receiver country")
    receiver_city: str = Field(None, description="Receiver's city")
    receiver_street: str = Field(None, description="Receiver street")
    articles: List[ArticleResponse] = Field(None, description="Articles")
    weather: dict = Field(None, description="The weather condition")
