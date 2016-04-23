import os
import requests
import operator
import re
import sys
from library import ScraperManager as sm
from scrapers import YellowstoneOrion
from flask import Flask, render_template, request
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job

from worker import conn

print(sm)
print(YellowstoneOrion)
# print(sys.modules)
# print(sm)

q = Queue(connection=conn)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
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

@app.route('/results/<job_key>', methods=['GET'])
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

# @app.route('/scrapers', methods=['GET'])
# def scrapers_list():


if __name__ == '__main__':
    app.run()
