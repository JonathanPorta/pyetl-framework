import os
import requests
import operator
import re
import sys
sys.setrecursionlimit(10000)
from library import ScraperManager as sm
from scrapers import YellowstoneOrion
from flask import Flask, render_template, request, jsonify
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job

from worker import conn

# print(sm)
# print(YellowstoneOrion)
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
        print("made it here")
        master_data = jsonify(job.result)
    else:
        master_data =  "Nay!", 202
    return render_template('../../results.html', master_data=master_data)
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


        return master_data



if __name__ == '__main__':
    app.run()
