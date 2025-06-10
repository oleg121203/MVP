from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.database import Base

class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    price = Column(Float, index=True)
    timestamp = Column(DateTime, index=True)
    source = Column(String, index=True)
    
    # Performance indexes for common queries
    __table_args__ = (
        Index('idx_pricedata_product_timestamp', 'product_id', 'timestamp'),
        Index('idx_pricedata_source_timestamp', 'source', 'timestamp'),
        Index('idx_pricedata_price_range', 'price'),
    )
