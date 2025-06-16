from abc import ABC, abstractmethod

class ScrapingJobServiceInterface(ABC):
    @abstractmethod
    def trigger_scraping_job(self) -> str:
        '''Triggers a scraping job and returns a message or task ID.'''
        pass
