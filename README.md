# pyscrape

### Setup Local Dev
Install python, virtualenv and deps. To get started go [here](https://realpython.com/blog/python/flask-by-example-part-1-project-setup).

Once

Then: `pip install -r requirements.txt`

### Pushing to Production/Staging on Heroku (Don't do this, ci should do this)
This is an example of how a sample app would deploy. This shouldn't be here.
git remote add heroku-staging git@heroku.com:pyscrape-staging.git
git remote add heroku-production git@heroku.com:pyscrape-production.git
Or
`make deploy`

### Release
First, create a new pip package. This will bump the patch version and write it to `VERSION`.
`make package`

Then, to push to the package to the repository:
`make release`

### Usage
Pyetl is meant as a framework to help with the extraction, transformation and loading of data between sources.

To get started, create a new Python project and then `pip install pypscraper-framework`.

To run the app flask app frontend: `pyetl_flask`
To run the worker process: `pyetl_worker`

The following two environment vars are required:
```
export APP_SETTINGS='DevelopmentConfig' # name of the corresponding config class for this env.
export APP_BASEDIR=$(pwd) # must point to directory containing your config file.
```

A config file is also required. See `config.py.example`.

### Concepts
The framework relies heavily on naming conventions and magically imports.
#### Pipe
This represents the flow of data from a source to a target. `pipe.start()` should do whatever is necessary determine and enqueue any and all `ETLJob`s that must execute in order for a run to be considered succesfull.

#### ETLJob
A base class defined in the framework. It has three methods: extract, transform, load.

#### Transformer/Extractor/Loader
Extend this class with a class that has the same name as your pipe's class. The ETLJob will run `{Transformer|Extractor|Loader}.execute()` when executing.
