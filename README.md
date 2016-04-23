# pyscrape

### Setup Local Dev
Install python, virtualenv and deps. To get started go [here](https://realpython.com/blog/python/flask-by-example-part-1-project-setup).

Once

Then: `pip install -r requirements.txt`

### Pushing to Production/Staging on Heroku (Don't do this, ci should do this)
git remote add heroku-staging git@heroku.com:pyscrape-staging.git
git remote add heroku-production git@heroku.com:pyscrape-production.git
Or
`make deploy`
