from .app import App as App
from .worker import Worker as Worker
from .lib import Scraper as Scraper
from .lib import ScrapeJob as ScrapeJob

def run_flask():
    App.run()

def run_worker():
    Worker.run()
