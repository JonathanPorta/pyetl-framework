import os
import requests
import operator
import re
import sys
from lib import ScraperManager

from flask import Flask, render_template, request
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job

from worker import conn

# print(sm)
# print(YellowstoneOrion)
# print(library)
# print(sys.modules)
print("__name__: ", __name__)

# Define App - import App from app
# from flask import Flask
App = Flask(__name__)
App.config.from_object(os.environ['APP_SETTINGS'])

q = Queue(connection=conn)


@App.route('/', methods=['GET', 'POST'])
def index():
    job_id = ""
    if request.method == 'POST':
        url = request.form['url']
        job = q.enqueue_call(
            func=scrape, args=(url,), result_ttl=5000
        )
        job_id = job.get_id()
        print(job_id)

    return render_template('index.html', job_id=job_id)

@App.route('/results/<job_key>', methods=['GET'])
def results_job_key(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202

def scrape(url):
    # Get the url that they entered
    try:
        r = requests.get(url)
    except Exception as e:
        print("Unable to get URL: {}".format(e))
    # Process the HTML in the requst using BeautifulSoup
    if r:
        raw = BeautifulSoup(r.text, 'html.parser')
        tags = raw.find_all('a')
        print(tags)
        return tags

@App.route('/scrapers', methods=['GET'])
def scrapers_list():
    sm = ScraperManager(App)
    scrapers = sm.list_scrapers()
    return render_template('scrapers.html', scrapers=scrapers)

@App.route('/scrapers/<name>', methods=['GET'])
def scrapers_detail(name):
    sm = ScraperManager(App)
    scraper = sm.load_scraper(name)
    scraper.start()
    return render_template('scraper.html', scraper=scraper)

if __name__ == '__main__':
    App.run()
