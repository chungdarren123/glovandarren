import pytest
from fastapi.testclient import TestClient
from main import app # Your FastAPI app
from app.models.scraped_data import ScrapedData
from app.models.deep_model_result import DeepModelResult
from sqlalchemy.orm import Session

# client fixture is from conftest.py

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Algorithmic Engine API. See /docs for documentation."}

def test_read_scraped_data_empty(client: TestClient, db_session: Session):
    response = client.get("/data/scraped/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["results"] == []

def test_read_scraped_data_with_items(client: TestClient, db_session: Session):
    sd1 = ScrapedData(url="http://api.test/1", content="API test 1")
    sd2 = ScrapedData(url="http://api.test/2", content="API test 2")
    db_session.add_all([sd1, sd2])
    db_session.commit()

    response = client.get("/data/scraped/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["results"]) == 2
    assert data["results"][0]["url"] == "http://api.test/1"

def test_read_deep_model_results_empty(client: TestClient, db_session: Session):
    response = client.get("/data/results/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["results"] == []

def test_read_deep_model_results_with_items(client: TestClient, db_session: Session):
    sd1 = ScrapedData(url="http://api.dmr.test/1", content="DMR test 1")
    db_session.add(sd1)
    db_session.commit() # Commit to get sd1.id

    dmr1 = DeepModelResult(scraped_data_id=sd1.id, score=0.75, label="good")
    db_session.add(dmr1)
    db_session.commit()

    response = client.get("/data/results/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["results"]) == 1
    assert data["results"][0]["label"] == "good"
    assert data["results"][0]["scraped_data_id"] == sd1.id
