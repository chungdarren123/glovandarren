from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
import uvicorn
from database import get_db, SessionLocal
from models import Base, Product, ESGScore
from services import (
    CarbonInterfaceService,
    SustainalyticsService,
    MSCIESGService,
    EconomicService,
    ESGScoringService
)

app = FastAPI()

# Allow all origins for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
carbon = CarbonInterfaceService()
sustainalytics = SustainalyticsService()
msci = MSCIESGService()
economic = EconomicService()
scoring = ESGScoringService()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=SessionLocal().bind)

@app.post("/products/")
def create_product(name: str, barcode: str, db: Session = Depends(get_db)):
    product = Product(name=name, barcode=barcode)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products/search/")
def search_products(q: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(
        (Product.name.ilike(f"%{q}%")) | 
        (Product.barcode == q)
    ).limit(5).all()

@app.post("/products/{product_id}/calculate")
def calculate_score(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    
    # Get scores from APIs
    env = carbon.get_carbon_footprint(f"prod_{product_id}")
    soc = sustainalytics.get_social_score(f"comp_{product_id}")
    gov = msci.get_governance_score(f"US{product_id}1234")
    econ = economic.get_economic_score(f"comp_{product_id}")
    
    # Calculate weighted score
    scores = scoring.calculate_weighted_score(env, soc, gov, econ)
    
    # Store result
    esg_score = ESGScore(
        product_id=product_id,
        **scores
    )
    db.add(esg_score)
    db.commit()
    
    return esg_score

@app.get("/barcode/{barcode}/score")
def get_score_by_barcode(barcode: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.barcode == barcode).first()
    if not product:
        raise HTTPException(404, "Product not found")
    
    score = db.query(ESGScore).filter(
        ESGScore.product_id == product.id
    ).order_by(ESGScore.calculated_at.desc()).first()
    
    if not score:
        raise HTTPException(404, "No scores available")
    
    return {
        "product": product.name,
        "barcode": product.barcode,
        "scores": {
            "environmental": score.environmental_score,
            "social": score.social_score,
            "governance": score.governance_score,
            "economic": score.economic_score,
            "overall": score.overall_score
        },
        "last_updated": score.calculated_at
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
