from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    barcode = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ESGScore(Base):
    __tablename__ = "esg_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    environmental_score = Column(Float)
    social_score = Column(Float)
    governance_score = Column(Float)
    economic_score = Column(Float)
    overall_score = Column(Float)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
