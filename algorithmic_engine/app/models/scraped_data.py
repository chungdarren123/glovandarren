from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint
from sqlalchemy.sql import func
from ..database.connection import Base # Adjusted import path

class ScrapedData(Base):
    __tablename__ = "scraped_data"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('url', name='uq_url'),)

    def __repr__(self):
        return f"<ScrapedData(id={self.id}, url='{self.url[:30]}...', timestamp='{self.timestamp}')>"
