import pytest
from sqlalchemy.exc import IntegrityError
from app.models.scraped_data import ScrapedData
from datetime import datetime

def test_create_scraped_data(db_session):
    url = "http://example.com/test"
    content = "Test content"
    data = ScrapedData(url=url, content=content, timestamp=datetime.utcnow())
    db_session.add(data)
    db_session.commit()

    retrieved = db_session.query(ScrapedData).filter_by(url=url).first()
    assert retrieved is not None
    assert retrieved.content == content
    assert retrieved.id is not None

def test_scraped_data_unique_url(db_session):
    url = "http://example.com/unique"
    data1 = ScrapedData(url=url, content="Content 1")
    db_session.add(data1)
    db_session.commit()

    data2 = ScrapedData(url=url, content="Content 2")
    db_session.add(data2)
    with pytest.raises(IntegrityError): # Or OperationalError depending on SQLAlchemy version/exact timing
        db_session.commit()
