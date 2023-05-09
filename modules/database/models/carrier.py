from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from modules.database.models.utility_model import TimeStampMixin
from modules.utilities.database import Base


class Carrier(Base, TimeStampMixin):
    __tablename__ = "carriers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    shipments = relationship("Shipment", back_populates="carrier")
