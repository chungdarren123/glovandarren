from sqlalchemy.orm import sessionmaker
from ..database.connection import SessionLocal, engine # Use SessionLocal
from ..models.scraped_data import ScrapedData
from scrapy.exceptions import DropItem
from datetime import datetime

class DatabasePipeline:
    def __init__(self, session_factory=None):
        self.Session = session_factory if session_factory else SessionLocal

    def open_spider(self, spider):
        # Potentially create tables here if not done globally, but init_db.py handles it
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        session = self.Session() # For testing, this can be the test_db_session
        is_external_session = (self.Session != SessionLocal)

        try:
            # Check if URL already exists
            exists = session.query(ScrapedData).filter_by(url=item['url']).first()
            if exists:
                spider.log(f"URL already exists in DB, skipping: {item['url']}")
                raise DropItem(f"Duplicate item found: {item['url']}") # This exception will be caught by Scrapy

            # If not a duplicate, proceed to add
            scraped_data_entry = ScrapedData(
                url=item['url'],
                content=item['content'],
                timestamp=item.get('timestamp', datetime.utcnow())
            )
            session.add(scraped_data_entry)
            session.commit() # Try to commit the new item
            spider.log(f"Saved item to DB: {item['url']}")

        except DropItem: # Specifically catch DropItem if it was from the duplicate check
            raise # Re-raise it for Scrapy to handle
        except Exception as e: # Catch other exceptions, possibly during commit of new item
            try:
                session.rollback() # Rollback this session if commit failed
            except Exception as rb_exc:
                spider.log(f"Rollback failed for item {item['url']}: {rb_exc}")
            spider.log(f"Failed to save item to DB: {item['url']}. Error: {e}")
            # Convert other DB errors to DropItem for Scrapy
            raise DropItem(f"Database error processing item {item['url']}: {e}")
        finally:
            # Only close the session if it was created by this pipeline instance using SessionLocal
            # If an external session factory (like for tests) was injected, let the injector manage its lifecycle.
            if not is_external_session and session:
                session.close()
        return item
