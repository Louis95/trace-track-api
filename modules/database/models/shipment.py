from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from modules.database.models.utility_model import TimeStampMixin
from modules.utilities.database import Base


class Shipment(Base, TimeStampMixin):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String, unique=True, nullable=False)
    sender_zip = Column(String)
    sender_country = Column(String)
    sender_city = Column(String)
    sender_street = Column(String)
    receiver_zip = Column(String, nullable=False)
    receiver_country = Column(String)
    receiver_city = Column(String, nullable=False)
    receiver_street = Column(String, nullable=False)
    carrier_id = Column(Integer, ForeignKey("carriers.id"))
    carrier = relationship("Carrier", back_populates="shipments")
    articles_on_shipment = relationship("ArticlesOnShipment", back_populates="shipment")


class ArticlesOnShipment(Base, TimeStampMixin):
    __tablename__ = "articles_on_shipment"

    shipment_id = Column(Integer, ForeignKey("shipments.id"), primary_key=True)
    shipment = relationship("Shipment", back_populates="articles_on_shipment")
    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    article = relationship("Article", back_populates="articles_on_shipment")
    quantity = Column(Integer, default=1)
