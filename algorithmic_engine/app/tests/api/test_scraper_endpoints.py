import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# client fixture from conftest.py

@patch('app.services.scraping_service.SubprocessScrapingJobService.trigger_scraping_job')
def test_trigger_scraper(mock_trigger_scraping_job, client: TestClient):
    mock_trigger_scraping_job.return_value = "Mocked: Scraper process initiated with PID: 12345"

    response = client.post("/scraper/scrape/")

    assert response.status_code == 200
    json_response = response.json()
    assert "Mocked: Scraper process initiated with PID: 12345" in json_response["message"]
    mock_trigger_scraping_job.assert_called_once()

@patch('app.services.scraping_service.SubprocessScrapingJobService.trigger_scraping_job')
def test_trigger_scraper_failure(mock_trigger_scraping_job, client: TestClient):
    mock_trigger_scraping_job.return_value = "Mocked: An error occurred"

    response = client.post("/scraper/scrape/")

    assert response.status_code == 200 # The endpoint itself doesn't throw 500 for this user message
    json_response = response.json()
    assert "Mocked: An error occurred" in json_response["message"]
    mock_trigger_scraping_job.assert_called_once()
