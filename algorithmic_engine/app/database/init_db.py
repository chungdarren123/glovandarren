from .connection import Base, engine
from ..models.scraped_data import ScrapedData
from ..models.deep_model_result import DeepModelResult

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created.")
