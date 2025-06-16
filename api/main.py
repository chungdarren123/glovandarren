from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI(title="Sustainability API")

# -- Models --
class ProductRequest(BaseModel):
    url: str

class SustainabilityScore(BaseModel):
    score: int
    review: str
    confidence: float

class Product(BaseModel):
    product_name: str
    category: str
    price: float

class AlternativeProduct(BaseModel):
    name: str
    score: int
    url: str

class ProductResponse(BaseModel):
    product_name: str
    score: SustainabilityScore
    alternatives: List[AlternativeProduct]

# --- Mock Scraper ---
async def scrape_product_data(url: str) -> dict:
    """Simulates scraping product data from a URL."""
    await asyncio.sleep(1)  # Simulate network delay
    return {
        "product_name": "Nike Organic Cotton T-Shirt",
        "category": "fashion",
        "price": 39.99,
    }

# --- Mock ML Model ---
def predict_sustainability(product_data: dict) -> dict:
    """Simulates an ML model generating a sustainability score."""
    return {
        "score": 82,
        "review": "Uses organic cotton but lacks fair-trade certification.",
        "confidence": 0.89
    }

# --- Mock Alternatives Generator ---
def get_alternatives(product_data: dict) -> List[dict]:
    """Simulates fetching eco-friendly alternatives."""
    alternatives_db = [
        {"name": "Patagonia T-Shirt", "score": 92, "url": "https://patagonia.com/tshirt"},
        {"name": "Eileen Fisher Organic Top", "score": 95, "url": "https://eileenfisher.com/top"}
    ]
    return alternatives_db

# -- API ENDPOINTS --

# Generate product review from product url
@app.post("/api/sustainability", response_model=ProductResponse)
async def get_sustainability(product_request: ProductRequest):
    url = product_request.url

    # Scrape url for product data
    try:
        product_data = await scrape_product_data(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping failed: {str(e)}")
    
    # Generate sustainability score
    sustainability_score = predict_sustainability(product_data)

    # Generate product alternatives
    alternatives = get_alternatives(product_data)

    # Cache data

    return {
        "product_name": product_data["product_name"],
        "sustainability_score": sustainability_score,
        "alternatives": alternatives
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
