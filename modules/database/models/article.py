from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from modules.database.models.utility_model import TimeStampMixin
from modules.utilities.database import Base


class Article(Base, TimeStampMixin):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String)
    price = Column(Float, default=0)
    articles_on_shipment = relationship("ArticlesOnShipment", back_populates="article")
