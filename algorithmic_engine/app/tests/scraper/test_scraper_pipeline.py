import pytest
from app.scraper.pipelines import DatabasePipeline
from app.scraper.items import ScrapedTextItem
from app.models.scraped_data import ScrapedData
from sqlalchemy.orm import Session
from scrapy.exceptions import DropItem
from datetime import datetime

@pytest.fixture
def pipeline(db_session: Session): # Inject db_session here
    # Pass a factory that returns the existing test session
    return DatabasePipeline(session_factory=lambda: db_session)

@pytest.fixture
def mock_spider():
    class MockSpider:
        def log(self, message):
            print(message) # Or use a logger
    return MockSpider()

def test_pipeline_process_item_new(pipeline, mock_spider, db_session: Session):
    url = "http://pipeline.test/new_item"
    timestamp = datetime.utcnow()
    item = ScrapedTextItem({'url': url, 'content': 'New pipeline content', 'timestamp': timestamp})

    pipeline.process_item(item, mock_spider)

    saved_item = db_session.query(ScrapedData).filter_by(url=url).first()
    assert saved_item is not None
    assert saved_item.content == 'New pipeline content'
    assert saved_item.url == url
    # assert saved_item.timestamp == timestamp # Check precision or convert for comparison

def test_pipeline_process_item_duplicate(pipeline, mock_spider, db_session: Session):
    url = "http://pipeline.test/duplicate_item"
    # Pre-insert an item
    existing_data = ScrapedData(url=url, content="Existing content")
    db_session.add(existing_data)
    db_session.commit()

    item = ScrapedTextItem({'url': url, 'content': 'Attempting to add duplicate'})

    with pytest.raises(DropItem) as excinfo:
        pipeline.process_item(item, mock_spider)
    assert "Duplicate item found" in str(excinfo.value)

    # Ensure no new item was added, and the old one is still there
    count = db_session.query(ScrapedData).filter_by(url=url).count()
    assert count == 1
