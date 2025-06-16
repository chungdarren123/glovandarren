from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base # Adjusted import path

class DeepModelResult(Base):
    __tablename__ = "deep_model_results"

    id = Column(Integer, primary_key=True, index=True)
    scraped_data_id = Column(Integer, ForeignKey("scraped_data.id"), nullable=False)
    score = Column(Float, nullable=False)
    label = Column(String, nullable=False)

    scraped_data = relationship("ScrapedData")

    def __repr__(self):
        return f"<DeepModelResult(id={self.id}, scraped_data_id={self.scraped_data_id}, score={self.score}, label='{self.label}')>"
