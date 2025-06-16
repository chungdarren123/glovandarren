from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- ScrapedData Schemas ---
class ScrapedDataBase(BaseModel):
    url: str
    content: Optional[str] = None

class ScrapedDataCreate(ScrapedDataBase):
    pass

class ScrapedData(ScrapedDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- DeepModelResult Schemas ---
class DeepModelResultBase(BaseModel):
    score: float
    label: str

class DeepModelResultCreate(DeepModelResultBase):
    scraped_data_id: int

class DeepModelResult(DeepModelResultBase):
    id: int
    scraped_data_id: int
    # Optionally include related ScrapedData for richer responses
    # scraped_data: ScrapedData

    class Config:
        from_attributes = True

# --- Pagination Schemas ---
class PaginatedResponse(BaseModel):
    total: int
    page: int
    size: int
    # results: List[BaseModel] # This will be specialized in the routers

class PaginatedScrapedData(PaginatedResponse):
    results: List[ScrapedData]

class PaginatedDeepModelResult(PaginatedResponse):
    results: List[DeepModelResult]

# --- Scraper Trigger Schema ---
class ScraperTriggerResponse(BaseModel):
    message: str
    task_id: Optional[str] = None # For potential background task ID
