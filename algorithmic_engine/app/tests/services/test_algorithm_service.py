import pytest
from app.services.algorithm_service import simple_text_algorithm, process_scraped_data
from app.models.scraped_data import ScrapedData
from app.models.deep_model_result import DeepModelResult
from app.tests.conftest import clear_tables # Helper if needed

def test_simple_text_algorithm():
    score, label = simple_text_algorithm("Short content.") # len 14 + ~15 for "Title: X\n" = ~29
    assert label == "short"

    long_text = "Title: Long\n" + ("a" * 150) # ~15 + 150 = 165
    score, label = simple_text_algorithm(long_text)
    assert label == "medium" # Based on current thresholds

    very_long_text = "Title: Very Long\n" + ("b" * 250) # ~20 + 250 = 270
    score, label = simple_text_algorithm(very_long_text)
    assert label == "long"

def test_process_scraped_data(db_session):
    # clear_tables(db_session) # Ensure clean state

    # Add some scraped data
    sd1 = ScrapedData(url="http://test.com/1", content="Some test content for processing.")
    sd2 = ScrapedData(url="http://test.com/2", content="Short.")
    db_session.add_all([sd1, sd2])
    db_session.commit()

    process_scraped_data(db_session)

    results = db_session.query(DeepModelResult).all()
    assert len(results) == 2

    r1 = db_session.query(DeepModelResult).filter_by(scraped_data_id=sd1.id).first()
    assert r1 is not None
    assert r1.label == "short" # Content "Some test content for processing." (len 33) is "short"

    r2 = db_session.query(DeepModelResult).filter_by(scraped_data_id=sd2.id).first()
    assert r2 is not None
    assert r2.label == "short" # "Short." + "Title: X\n" likely short

    # Run again, should not process anything new
    process_scraped_data(db_session)
    results_after_second_run = db_session.query(DeepModelResult).count()
    assert results_after_second_run == 2
