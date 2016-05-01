from .app import App as App
from .worker import Worker as Worker
from .lib import Scraper as Scraper

def run_flask():
    App.run()

def run_worker():
    Worker.run()
