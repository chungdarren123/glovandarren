from sqlalchemy.orm import Session, joinedload
from .algorithm_strategy import AlgorithmStrategy # Added for OCP structure
from ..database.connection import SessionLocal, get_db # Assuming get_db can be used if needed, or SessionLocal directly
from ..models.scraped_data import ScrapedData
from ..models.deep_model_result import DeepModelResult

def simple_text_algorithm(content: str) -> tuple[float, str]:
    '''
    A simple placeholder algorithm. Conceptually, this function could be an implementation of an AlgorithmStrategy.
    Score: length of the content.
    Label: based on content length.
    '''
    if content is None:
        length = 0
    else:
        length = len(content)

    score = float(length)

    if length < 100: # Assuming "Title: X\nBody text..." is the format
        label = "short"
    elif length < 200:
        label = "medium"
    else:
        label = "long"

    return score, label

def process_scraped_data(db: Session):
    '''
    Processes ScrapedData records that don't have a DeepModelResult yet.
    '''
    # Find ScrapedData records that do not have a corresponding DeepModelResult
    # This can be done using a left join and filtering where the right side is NULL.
    scraped_data_without_results = db.query(ScrapedData).outerjoin(DeepModelResult, ScrapedData.id == DeepModelResult.scraped_data_id).filter(DeepModelResult.id == None).all()

    if not scraped_data_without_results:
        print("No new scraped data to process.")
        return

    print(f"Found {len(scraped_data_without_results)} new scraped data records to process.")

    for data_item in scraped_data_without_results:
        print(f"Processing ScrapedData ID: {data_item.id}, URL: {data_item.url}")

        score, label = simple_text_algorithm(data_item.content)

        new_result = DeepModelResult(
            scraped_data_id=data_item.id,
            score=score,
            label=label
        )
        db.add(new_result)

        try:
            db.commit()
            print(f"Saved DeepModelResult for ScrapedData ID: {data_item.id} with Score: {score}, Label: {label}")
        except Exception as e:
            db.rollback()
            print(f"Error saving DeepModelResult for ScrapedData ID: {data_item.id}. Error: {e}")

def run_algorithm_service():
    '''
    Main function to run the algorithm service.
    '''
    print("Algorithm service started...")
    db = SessionLocal()
    try:
        process_scraped_data(db)
    finally:
        db.close()
    print("Algorithm service finished.")

if __name__ == "__main__":
    # This allows running the service independently for testing
    # Ensure Python path is set up if running from project root:
    # python -m app.services.algorithm_service
    import os
    import sys
    # Add project root to Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from app.database.init_db import create_tables # Ensure tables exist
    create_tables()

    run_algorithm_service()
