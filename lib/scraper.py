import os

class Scraper():
    def __init__(self, scraper_manager, name):
        print('scraper.py::init() - the base class.')
        self.scraper_manager = scraper_manager
        self.name = name

    def start(self):
        print('scraper.py::start() - the base class.')
