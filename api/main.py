from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conlist
from typing import List
from dotenv import load_dotenv
import os
import time

# Initialise FastAPI app
app = FastAPI(
    title="Product Sustainability API", 
    description="API to analyse sustainability of a product based on carbon footprint, social and environmental metrics"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://sustainability-extension"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

# Security configuration
load_dotenv(".env.local")
api_key_header = APIKeyHeader(name="Sustainability-API-KEY")

# Load ML Model
analyzer = SustainabilityAnalyzer()

# -- DATA MODELS --
class ProductInput(BaseModel):
    product_name: str
    price: float

class SustainabilityScore(BaseModel):
    score: int
    review: str
    confidence: float

class AlternativeProduct(BaseModel):
    alt_product_name: str
    score: SustainabilityScore
    url: str

class ProductResponse(BaseModel):
    product_name: str
    score: SustainabilityScore
    alternatives: List[AlternativeProduct]

class AnalysisResponse(BaseModel):
    results: List[ProductResponse]
    processing_time_ms: int

class ErrorResponse(BaseModel):
    error_message: str

# -- HELPER FUNCTION --
async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# -- API ENDPOINTS --

# Generate product reviews from list of product names
@app.post(
        "/api/analyze/products", 
        response_model=ProductResponse,
        summary="Analyze product sustainability",
        description="Process a list of product names to generate their sustainability scores and review"
        )
async def analyze_products(
    request: Request,
    products = conlist(ProductInput, min_items=1, max_items=100),
    language = "en",
    api_key: str = Depends(verify_api_key)
):
    start_time = time.time()

    try:
        results = []
        for product in products:
            analysis = analyzer.analyze(
                product.name
            )

            results.append(ProductResponse(
                product_name=product.name,
                **analysis
            ))
        
        return {
            "results": results,
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)