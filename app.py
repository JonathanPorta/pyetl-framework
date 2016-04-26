import os
import requests
import operator
import re
import sys
sys.setrecursionlimit(10000)
from lib import ScraperManager

from flask import Flask, render_template, request, jsonify
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job

from worker import conn

# Define App
App = Flask(__name__) # Todo: Understand why we use __name__ here.
App.config.from_object(os.environ['APP_SETTINGS'])
App.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension') # Jade template support

q = Queue(connection=conn)

@App.route('/', methods=['GET', 'POST'])
def index():
    job_id = ""
    if request.method == 'POST':
        url = request.form['url']
        job = q.enqueue('workers.YellowstoneOrion')
        #     func=scrape, args=(url,), result_ttl=5000
        # )
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
    # Get the url that they entered
    try:
        r = requests.get(url)
    except Exception as e:
        print("Unable to get URL: {}".format(e))
    # Process the HTML in the requst using BeautifulSoup
    if r:
        html = r.content.decode('ascii', 'ignore')
        raw = BeautifulSoup(html, "lxml")
        raw = raw.prettify()
        soup = BeautifulSoup(raw,"lxml")
        tags = soup.find_all('td')
        sections = soup.find_all('bgcolor="#F2E3B8"')

        owner_fields = ['Primary Owner','Tax ID','Geo Code','Property Address','Legal Description','Property Type']
        site_fields = ['Neighborhood Code','Parking type','Utilities','Lot Size','Location','Fronting','Parking Prox','Access','Topography']
        owner_info = {}
        site_info = {}
        master_data_sections = []
        master_data = {}
        tagsections = soup.find_all('td', {'bgcolor' : '#F2E3B8'})

        for j,k in enumerate(tagsections):
            print(k)
            master_data_sections.append(k)
        for i,e in enumerate(tags):

            d = str(e)

            for field in owner_fields:
                if field in d:
                    field_value = str(tags[i+1].text.strip())
                    field_value = re.sub('[^a-zA-Z0-9-_*. ,]', '', field_value)
                    owner_info[field] = field_value
            for field in site_fields:
                if field in d:
                    field_value = str(tags[i+1].text.strip())
                    field_value = re.sub('[^a-zA-Z0-9-_*. ,]', '', field_value)
                    site_info[field] = field_value

        for sections in master_data_sections:
            master_data[sections] = eval(sections)

        master_data = {"fuck you":False}
        return master_data

@App.route('/scrapers', methods=['GET'])
def scrapers_list():
    sm = ScraperManager(App)
    scrapers = sm.list_scrapers()
    return render_template('scrapers.jade', scrapers=scrapers)

@App.route('/scrapers/<name>', methods=['GET'])
def scrapers_detail(name):
    sm = ScraperManager(App)
    scraper = sm.load_scraper(name)
    scraper.start()
    return render_template('scraper.jade', scraper=scraper)

if __name__ == '__main__':
    App.run()
