import os
import requests
import operator
import re
import sys
sys.setrecursionlimit(10000)
from pyscraper_framework.lib import ScraperManager

from flask import Flask, render_template, request, jsonify
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from importlib.machinery import SourceFileLoader

from pyscraper_framework.worker import conn

# Define App
App = Flask(__name__)
# Load app config from file
config_module = SourceFileLoader('config', "{}/config.py".format(os.environ['APP_BASEDIR'])).load_module()
config = getattr(config_module, os.environ['APP_SETTINGS'])

App.config.from_object(config)
App.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension') # Jade template support

# init our scraper manager - the magic maker that loads our scrapers.
scraper_manager = ScraperManager(App)
scraper_manager.load() # blocking call that loads scrapers from FS.

q = Queue(connection=conn)

@App.route('/', methods=['GET', 'POST'])
def index():
    job_id = ""
    if request.method == 'POST':
        url = request.form['url']
        # job = q.enqueue('workers.YellowstoneOrion', args=(True))
        # #     func=scrape, args=(url,), result_ttl=5000
        # # )
        job = q.enqueue_call(
            func=YellowstoneOrion().execute, args=[url], result_ttl=5000
        )

        job_id = job.get_id()
        print(job_id)

    return render_template('index.jade', job_id=job_id)

@App.route('/results/<job_key>', methods=['GET'])
def results_job_key(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        print("made it here")
        master_data = job.result
    else:
        master_data =  "Nay!", 202
    return jsonify(master_data)

def scrape(url):
    # TODO: Removed actual scraping code for testing
    master_data = {"url": url}
    return master_data

@App.route('/scrapers', methods=['GET'])
def scrapers_list():
    scrapers = scraper_manager.get_scrapers()
    print(scraper_manager._jobs)
    print('scrapers: ', scrapers)
    return render_template('scrapers.jade', scrapers=scrapers.values())

@App.route('/scrapers/<name>', methods=['GET'])
def scraper_detail(name):
    scraper = scraper_manager.init_scraper(name)
    return render_template('scraper.jade', scraper=scraper)

@App.route('/scrapers/<name>/start', methods=['GET'])
def scraper_start(name):
    scraper = scraper_manager.init_scraper(name)
    scraper.start(q)
    print("log shit")
    return render_template('scraper_start.jade', scraper=scraper)

if __name__ == '__main__':
    App.run()
