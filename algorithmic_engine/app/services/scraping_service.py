from .scraping_service_interface import ScrapingJobServiceInterface
import subprocess
import sys
import os

class SubprocessScrapingJobService(ScrapingJobServiceInterface):
    def _get_project_root(self):
        # Assuming this service file is in app/services/
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def trigger_scraping_job(self) -> str:
        project_root = self._get_project_root()
        scraper_script_path = os.path.join(project_root, "app", "scraper", "run_scraper.py")
        python_executable = sys.executable

        try:
            # Using Popen for non-blocking fire-and-forget
            process = subprocess.Popen([python_executable, scraper_script_path], cwd=project_root)
            message = f"Scraper process initiated with PID: {process.pid}. It runs independently."
            print(message) # For server logs
            return message
        except Exception as e:
            error_message = f"An unexpected error occurred while trying to run scraper: {e}"
            print(error_message) # For server logs
            # Depending on desired behavior, could raise an exception here to be caught by API
            return error_message
