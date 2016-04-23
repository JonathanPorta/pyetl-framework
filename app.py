import os
import requests
import operator
import re

from flask import Flask, render_template, request
from collections import Counter
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        # Get the url that they entered
        try:
            url = request.form['url']
            r = requests.get(url)
        except Exception as e:
            errors.append(
                "Unable to get URL: {}".format(e)
            )
        # Process the HTML in the requst using BeautifulSoup
        if r:
            raw = BeautifulSoup(r.text, 'html.parser')
            results = raw.find_all('a')

    return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def index_name(name):
    return "Hello {}".format(name)

if __name__ == '__main__':
    app.run()
