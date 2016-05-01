import os

class ScrapeJob():

    def __init__(self, url):
        self.url = url
        print("ScrapeJob base class")

    def execute(self):
        print('Scrape_Job.py::execute() - the base class.')

    def retrieve(self, url):
        print("retrieve")
        # Get the raw data from the webpage

    def parse(self, data):
        print("parse")
        # BeautifulSoup Here!

    def save(self, results):
        print("save")
        # put the results somewhere
