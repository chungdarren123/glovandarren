import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Add project root to Python path to allow absolute imports
# This assumes 'algorithmic_engine' is the project root and this script is in 'algorithmic_engine/app/scraper'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from app.scraper.spiders.basic_spider import BasicSpider # Direct import after path adjustment
from app.database.init_db import create_tables

def main():
    # Ensure tables are created before running the scraper
    print("Ensuring database tables exist...")
    create_tables()
    print("Database tables checked/created.")

    print("Starting scraper...")
    settings = get_project_settings()

    # Scrapy's get_project_settings() might not work as expected when not run via 'scrapy crawl'
    # Manually update settings if needed, especially paths
    settings.set('SPIDER_MODULES', ['app.scraper.spiders'])
    settings.set('NEWSPIDER_MODULE', 'app.scraper.spiders') # Corrected syntax
    settings.set('ITEM_PIPELINES', {'app.scraper.pipelines.DatabasePipeline': 300}) # Explicitly set pipeline
    # If settings.py is in the same directory as run_scraper.py, Scrapy might pick it up.
    # Otherwise, we might need to load it explicitly or ensure PYTHON_PATH includes 'app.scraper'

    process = CrawlerProcess(settings)
    process.crawl(BasicSpider)
    process.start() # the script will block here until the crawling is finished
    print("Scraping finished.")

if __name__ == '__main__':
    main()
