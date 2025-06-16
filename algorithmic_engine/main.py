from fastapi import FastAPI
from app.api.routers import data_router, scraper_router # Corrected import path
from app.database.init_db import create_tables # Corrected import path
import os
import sys

# This adjustment is important if main.py is in the project root
# It ensures that 'app' is discoverable as a package.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


app = FastAPI(title="Algorithmic Engine API")

@app.on_event("startup")
def on_startup():
    print("Creating database tables during startup...")
    create_tables() # This will use the DATABASE_URL from .env
    print("Database tables checked/created.")

app.include_router(data_router.router, prefix="/data", tags=["Data Retrieval"])
app.include_router(scraper_router.router, prefix="/scraper", tags=["Scraping"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Algorithmic Engine API. See /docs for documentation."}

# To run (from algorithmic_engine directory):
# uvicorn main:app --reload --port 8000
