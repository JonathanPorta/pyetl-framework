import os, sys, requests, re, operator
sys.setrecursionlimit(10000)
from pyetl_framework.lib import PipelineManager

from flask import Flask, render_template, request, jsonify
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from importlib.machinery import SourceFileLoader

from pyetl_framework.worker import conn

# Define App
App = Flask(__name__)

# Load app config from file
config_module = SourceFileLoader('config', os.path.join(os.environ['APP_BASEDIR'], 'config.py')).load_module()
config = getattr(config_module, os.environ['APP_SETTINGS'])

App.config.from_object(config)
App.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension') # Jade template support

# init our pipeline manager - the magic maker that loads our pipelines.
pipeline_manager = PipelineManager(App)
pipeline_manager.load() # blocking call that loads pipeline from FS.

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

@App.route('/pipelines', methods=['GET'])
def pipelines_list():
    pipelines = pipeline_manager.get_pipelines()
    print(pipeline_manager._pipelines)
    print(pipeline_manager._extractors)
    print(pipeline_manager._transformers)
    print(pipeline_manager._loaders)
    print('pipelines: ', pipelines)
    return render_template('pipelines.jade', pipelines=pipelines.values())

@App.route('/pipelines/<name>', methods=['GET'])
def pipeline_detail(name):
    pipeline = pipeline_manager.init_pipeline(name)
    return render_template('pipeline.jade', pipeline=pipeline)

@App.route('/pipelines/<name>/start', methods=['GET'])
def pipeline_start(name):
    pipeline = pipeline_manager.init_pipeline(name)
    pipeline.start(q)
    print("log shit")
    return render_template('pipeline_start.jade', pipeline=pipeline)

if __name__ == '__main__':
    App.run()
