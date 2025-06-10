from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime)
    source = Column(String)
