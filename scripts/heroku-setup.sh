#!/bin/bash

git remote add heroku-staging git@heroku.com:pyscrape-staging.git
git remote add heroku-production git@heroku.com:pyscrape-production.git

heroku config:set APP_SETTINGS=config.StagingConfig --remote heroku-staging
heroku config:set APP_SETTINGS=config.ProductionConfig --remote heroku-production
