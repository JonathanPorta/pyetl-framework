import os

class Scraper():
    def __init__(self, scraper_manager, name, job_class):
        print('scraper.py::init() - the base class.')
        self.scraper_manager = scraper_manager
        self.name = name
        self._job_class = job_class

    def init_job(self, *args, **kwargs):
        return self._job_class(*args, **kwargs)

    def start(self, queue):
        print('scraper.py::start() - the base class.',queue)
