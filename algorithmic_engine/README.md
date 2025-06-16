# Algorithmic Engine & Web Scraper API

This project is a scalable algorithmic engine with an integrated web scraper, persistence layer, and a FastAPI-based API for data delivery. It extracts data from web sources, processes it through a placeholder algorithm, stores the results, and makes both raw and processed data available via API endpoints.

## Features

- Web scraper (Scrapy) to extract data from URLs.
- Algorithmic processing of scraped data (placeholder logic).
- Data persistence using SQLAlchemy and SQLite.
- FastAPI backend providing RESTful API endpoints.
- Adherence to SOLID principles for maintainability and extensibility.
- Automated tests using Pytest.
- Containerized deployment using Docker and Docker Compose.

## Prerequisites

- Python 3.9+
- Pip (Python package installer)
- Docker
- Docker Compose

## Project Structure

```
algorithmic_engine/
├── app/                      # Core application module
│   ├── api/                  # FastAPI specific code (routers, schemas)
│   │   ├── routers/
│   │   └── schemas.py
│   ├── database/             # Database connection, initialization
│   │   ├── connection.py
│   │   └── init_db.py
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── scraped_data.py
│   │   └── deep_model_result.py
│   ├── scraper/              # Scrapy project
│   │   ├── spiders/
│   │   ├── items.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── run_scraper.py    # Script to run scraper
│   ├── services/             # Business logic (algorithm, scraping trigger)
│   │   ├── algorithm_service.py
│   │   ├── scraping_service.py
│   │   └── scraping_service_interface.py
│   └── tests/                # Automated tests (Pytest)
│       ├── api/
│       ├── models/
│       ├── scraper/
│       └── services/
│       └── conftest.py
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (DATABASE_URL)
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose setup
├── pytest.ini                # Pytest configuration
└── README.md                 # This file
```

## Setup and Running

### 1. Clone the Repository

```bash
git clone <repository_url>
cd algorithmic_engine
```

### 2. Environment Variables

Create a `.env` file in the `algorithmic_engine` root directory:

```env
DATABASE_URL=sqlite:///./sql_app.db
```
This is the default configuration. The `sql_app.db` file will be created in the root directory when running locally, or in the `/app_engine` directory when running in Docker (and persisted via a volume).

### 3. Local Development Setup (Without Docker)

#### a. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### b. Install Dependencies

```bash
pip install -r requirements.txt
```

#### c. Running the Application Locally

The FastAPI application uses Uvicorn as its ASGI server.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The API will be accessible at `http://localhost:8000`.
Interactive API documentation (Swagger UI) will be at `http://localhost:8000/docs`.
Alternative API documentation (ReDoc) will be at `http://localhost:8000/redoc`.

The database tables will be created automatically on startup if they don't exist.

### 4. Running with Docker (Recommended for Production-like Environment)

#### a. Build and Run Docker Containers

Ensure Docker and Docker Compose are installed and running.

```bash
cd algorithmic_engine  # Ensure you are in the project root
docker-compose up --build
```
This command will build the Docker image for the application and start the service defined in `docker-compose.yml`. The API will be accessible at `http://localhost:8000`.
The SQLite database file (`sql_app.db`) will be persisted in a Docker volume named `sqlite_data`.

To stop the containers:
```bash
docker-compose down
```

### 5. Running Standalone Scripts

#### a. Web Scraper

To run the web scraper independently (e.g., for a scheduled job or manual trigger):

```bash
# Ensure you are in the algorithmic_engine directory
# If using a venv, ensure it's activated: source venv/bin/activate
python app/scraper/run_scraper.py
```
This will scrape the predefined URLs and save data to the database specified by `DATABASE_URL`.

#### b. Algorithm Service

To process any newly scraped data:

```bash
# Ensure you are in the algorithmic_engine directory
# If using a venv, ensure it's activated: source venv/bin/activate
python -m app.services.algorithm_service
```
This will fetch unprocessed data from `ScrapedData`, apply the algorithm, and save results to `DeepModelResult`.

### 6. Running Tests

Tests are written using Pytest. They use a separate test database (`test_sql_app.db`) which is created and destroyed during the test session.

```bash
# Ensure you are in the algorithmic_engine directory
# If using a venv, ensure it's activated: source venv/bin/activate
python -m pytest -v
```

## API Endpoints

The API provides endpoints for triggering scraping and retrieving data. Base URL: `http://localhost:8000`

### Scraper API

- **POST /scraper/scrape/**
  - **Description**: Initiates a web scraping job. The scraper runs in the background.
  - **Request Body**: None
  - **Response (200 OK)**:
    ```json
    {
      "message": "Scraper process initiated with PID: <process_id>. It runs independently.",
      "task_id": null
    }
    ```
    (Note: `task_id` is currently null; PID is part of the message)

### Data Retrieval API

#### Scraped Data

- **GET /data/scraped/**
  - **Description**: Retrieves a paginated list of raw scraped data.
  - **Query Parameters**:
    - `url_contains` (string, optional): Filter by URL containing the given string.
    - `page` (integer, optional, default: 1): Page number for pagination.
    - `size` (integer, optional, default: 10): Number of items per page (max 100).
  - **Response (200 OK)**:
    ```json
    {
      "total": 2,
      "page": 1,
      "size": 10,
      "results": [
        {
          "url": "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
          "content": "Title: Mystery | Books to Scrape - Sandbox\nBody text could be extracted here...",
          "id": 1,
          "timestamp": "2023-10-27T10:00:00.000Z"
        }
        // ... more results
      ]
    }
    ```

#### Algorithm Results

- **GET /data/results/**
  - **Description**: Retrieves a paginated list of processed algorithm results.
  - **Query Parameters**:
    - `label` (string, optional): Filter by a specific result label (e.g., "short", "medium", "long").
    - `min_score` (float, optional): Filter by a minimum score.
    - `page` (integer, optional, default: 1): Page number for pagination.
    - `size` (integer, optional, default: 10): Number of items per page (max 100).
  - **Response (200 OK)**:
    ```json
    {
      "total": 1,
      "page": 1,
      "size": 10,
      "results": [
        {
          "score": 168.0,
          "label": "medium",
          "id": 1,
          "scraped_data_id": 1
        }
        // ... more results
      ]
    }
    ```

For live, interactive documentation, please visit `/docs` or `/redoc` when the application is running.

## SOLID Principles

This project attempts to adhere to SOLID principles:
- **SRP**: Components like database connection, models, individual API routers, scraper pipelines, and algorithm logic are separated.
- **OCP**: The algorithm service is designed to allow new algorithms (strategies) to be added without modifying existing service code (prepared via `AlgorithmStrategy` protocol). Scraper pipelines and FastAPI dependencies also support extension.
- **LSP**: Not heavily applicable with the current class structure, but would be important if more complex inheritance hierarchies were introduced.
- **ISP**: Pydantic schemas are specific. API routers provide focused interfaces.
- **DIP**: FastAPI's dependency injection promotes this (e.g., `get_db`). The scraper trigger service (`ScrapingJobServiceInterface`) abstracts the specific method of running scraping jobs.

## Potential Future Improvements

- **More Sophisticated Algorithm**: Replace the placeholder algorithm with a real model.
- **Advanced Scraper**: Implement more robust extraction logic, error handling, and dynamic URL discovery in the scraper.
- **Asynchronous Task Queue**: Use Celery or a similar system for managing scraping and algorithm processing tasks, especially for long-running jobs.
- **User Authentication/Authorization**: Secure API endpoints if needed.
- **Enhanced Filtering and Sorting**: Add more options for data retrieval.
- **Different Database**: Migrate to PostgreSQL or another production-grade database if SQLite limitations are hit.
- **CI/CD Pipeline**: Automate testing and deployment.
- **Monitoring and Logging**: Integrate more comprehensive logging and monitoring.
EOL
