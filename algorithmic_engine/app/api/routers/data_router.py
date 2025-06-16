from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from ...database.connection import get_db
from ...models.scraped_data import ScrapedData as DBScrapedData
from ...models.deep_model_result import DeepModelResult as DBDeepModelResult
from ..schemas import ScrapedData, DeepModelResult, PaginatedScrapedData, PaginatedDeepModelResult # Corrected import path

router = APIRouter()

@router.get("/scraped/", response_model=PaginatedScrapedData)
def read_scraped_data(
    db: Session = Depends(get_db),
    url_contains: Optional[str] = Query(None, description="Filter by URL containing this string"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    query = db.query(DBScrapedData)
    if url_contains:
        query = query.filter(DBScrapedData.url.contains(url_contains))

    total = query.count()
    offset = (page - 1) * size
    items = query.offset(offset).limit(size).all()

    return PaginatedScrapedData(
        total=total,
        page=page,
        size=size,
        results=items
    )

@router.get("/results/", response_model=PaginatedDeepModelResult)
def read_deep_model_results(
    db: Session = Depends(get_db),
    label: Optional[str] = Query(None, description="Filter by specific label"),
    min_score: Optional[float] = Query(None, description="Filter by minimum score"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    query = db.query(DBDeepModelResult).options(joinedload(DBDeepModelResult.scraped_data)) # Example of loading related data
    if label:
        query = query.filter(DBDeepModelResult.label == label)
    if min_score is not None:
        query = query.filter(DBDeepModelResult.score >= min_score)

    total = query.count()
    offset = (page - 1) * size
    items = query.offset(offset).limit(size).all()

    return PaginatedDeepModelResult(
        total=total,
        page=page,
        size=size,
        results=items
    )
