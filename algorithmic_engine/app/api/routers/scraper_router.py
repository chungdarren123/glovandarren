from fastapi import APIRouter, Depends, BackgroundTasks # Keep BackgroundTasks if other uses, or remove
from ..schemas import ScraperTriggerResponse # Corrected import path
from ...services.scraping_service_interface import ScrapingJobServiceInterface # Adjusted
from ...services.scraping_service import SubprocessScrapingJobService # Adjusted

router = APIRouter()

# Dependency for the scraping service
def get_scraping_service() -> ScrapingJobServiceInterface:
    return SubprocessScrapingJobService()

@router.post("/scrape/", response_model=ScraperTriggerResponse)
async def trigger_scraper(
    # background_tasks: BackgroundTasks, # Popen is already non-blocking from API perspective
    scraper_service: ScrapingJobServiceInterface = Depends(get_scraping_service)
):
    # The SubprocessScrapingJobService.trigger_scraping_job uses Popen,
    # which is non-blocking for the FastAPI endpoint.
    # No need for BackgroundTasks here if Popen is used correctly.
    message = scraper_service.trigger_scraping_job()
    # Check if message indicates an error (simple check)
    if "error occurred" in message or "failed" in message:
        # Consider returning a different HTTP status code for errors
        return ScraperTriggerResponse(message=message, task_id=None) # Or raise HTTPException
    return ScraperTriggerResponse(message=message) # task_id could be PID if useful
